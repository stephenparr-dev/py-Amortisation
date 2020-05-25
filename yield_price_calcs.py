import datetime as dt

class BgCalcs:

    def __init__(self):
        pass

    def next_prev_coupon_date(self, sett_date, mat_date, coup_freq):
        mth_mod = int(12 / coup_freq)

        ncd = sett_date.replace(month = mat_date.month, day = mat_date.day)
        if ncd > sett_date:
            pcdm = mat_date.month - mth_mod
            pcdy = sett_date.year
            if pcdm < 1:
                pcdy = pcdy - 1
                pcdm = pcdm + 12
            pcd = sett_date.replace(year = pcdy, month = pcdm, day = mat_date.day)
            if pcd < sett_date:
                return(pcd, ncd)
            else:
                while pcd > sett_date:
                    pcdm = pcdm - mth_mod
                    if pcdm < 1:
                        pcdy = pcdy - 1
                        pcdm = pcdm + 12
                    pcd = pcd.replace(year = pcdy, month = pcdm)
                if pcd.month + mth_mod > 12:
                    ncdmt = pcd.month + mth_mod - 12
                    ncdyt = pcd.year + 1
                    ncdt = pcd.replace(year = ncdyt, month = ncdmt)
                else:
                    ncdt = pcd.replace(month = pcd.month + mth_mod)
                if ncdt != ncd:
                    ncd = ncdt
                    return(pcd, ncd)
                else:
                    return(pcd,ncd)
        else:
            ncdm = ncd.month + mth_mod
            ncdy = ncd.year
            if ncdm > 12:
                ncdy = ncdy + 1
                ncdm = ncdm - 12
            while ncd < sett_date:
                ncdm = ncdm + mth_mod
                if ncdm > 12:
                    ncdy = ncdy + 1
                    ncdm = ncdm - 12
                ncd = ncd.replace(year = ncdy, month = ncdm)
            if ncd.month - mth_mod < 12:
                pcdm = ncd.month - mth_mod + 12
                pcdy = ncd.year - 1
                pcd = ncd.replace(year = pcdy, month = pcdm)
                return(pcd, ncd)
            else:
                pcd = ncd.replace(month = ncd.month - mth_mod)
                return(pcd, ncd)

    def actual_days_in_period(self, ncd, sett_date):
        dsca = ncd - sett_date
        dsca = dsca.days
        return dsca

    def max_days_in_period(self, acc_basis, coup_freq, dsca):
        if acc_basis == 0 or acc_basis == 4:
            maxd = int(360 / coup_freq)
            return maxd
        elif acc_basis == 2 and coup_freq == 1:
            maxd = 360
            return maxd
        else:
            maxd = dsca
            return maxd

    def days_settlement_to_next_coupon(self, dsca, maxd):
        if dsca.days > maxd:
            dsc = maxd
            return dsc
        else:
            dsc = dsca
            return dsc
    
    def days_settlement_to_redemption(self, mat_date, sett_date):
        dsr = mat_date - sett_date
        dsr = dsr.days
        return dsr
    
    def days_in_current_coupon_period(self, acc_basis, coup_freq, ncd, pcd):
        if acc_basis == 0 or acc_basis == 4:
            e = 360 / coup_freq
            return e
        elif acc_basis == 2 and coup_freq == 1:
            e = 360
            return e
        elif ncd.days - pcd.days == 366 and acc_basis == 3:
            e = 365
            return e
        else:
            e = ncd.days - pcd.days
            return e
    
    def coupons_from_settlement_to_maturity(self, ncd, mat_date, mth_mod):
        coupl = [ncd]
        cdate = ncd
        cdatey = ncd.year
        while cdate < mat_date:
            cdatem = cdate.month + mth_mod
            if cdatem > 12:
                cdatey = cdatey + 1
                cdatem = cdatem - 12
            cdate = cdate.replace(year = cdatey, month = cdatem)
            coupl.append(cdate)
        n = len(coupl)
        return n
    
    def days_start_coupon_period_to_settlement_date(self, e, dsc):
        a = e - dsc
        return a

    def red_yield(self, red_value, coupon, coup_freq, curr_price, a, e, dsr, dsc, n):
        parti = (red_value / 100 + coupon / coup_freq) - (curr_price / 100 + (a / e * coupon / coup_freq))
        partii = curr_price / 100 + (a / e * coupon / coup_freq)
        partiii = coup_freq * e / dsr

        eyl = []

        if partii != 0:
            ey = parti / partii * partiii
            eyl.append(ey)
        else:
            ey = 0
            eyl.append(ey)
        
        eyl.append(0.1)

        att = 0
        pp_delta = 0
        calc_p = 0

        while calc_p != curr_price:

            att = att + 1
            part1 = red_value / ((1 + eyl[att - 1] / coup_freq) ** (n - 1 + dsc / e))
            part2 = 0
            part3 = -100 * (coupon / coup_freq) * (a / e)

            cpn = 1

            while cpn <= n:
                pt2 = 100 * (coupon / coup_freq) / ((1 + eyl[att - 1] / coup_freq) ** (cpn - 1 + dsc / e))
                part2 = part2 + pt2
                cpn = cpn + 1
            
            calc_p = part1 + part2 + part3
            p_delta = curr_price - calc_p

            if att > 1:
                pd_move = pp_delta - p_delta
                if pd_move == 0:
                    break
                ydelta_pdmove = y_delta / pd_move
                y_next = eyl[att - 1] + (p_delta * ydelta_pdmove)
                eyl.append(y_next)

            y_delta = eyl[att] - eyl[att-1]
            pp_delta = p_delta

        red_yield = eyl[att - 1]
        return red_yield

    def calc_price(self, curr_yield, dsc, e, n, a, red_value, coup_freq, coupon):
        if n == 1:
            parta_p = 1 / (1 + (curr_yield / coup_freq) * (n - 1 + (dsc / e)))
            partb_p = parta_p * red_value
            partc_p = 100 * (coupon / coup_freq) * parta_p
            partd_p = -100 * (coupon / coup_freq) * (a / e)

            calc_pr = parta_p + partb_p + partc_p + partd_p
            return calc_pr
        else:
            part1_p = red_value / (1 + curr_yield / coup_freq) ** ((n - 1) + dsc / e)
            part2_p = 0
            cp = 1
            while cp <=n:
                pt2_p = 100 * (coupon / coup_freq) / ((1 + curr_yield / coup_freq) ** (cp - 1 + dsc / e))
                part2_p = part2_p + pt2_p
                cp = cp + 1
            part3_p = -100 * (coupon / coup_freq) * (a / e)

            calc_pr = part1_p + part2_p + part3_p
            return calc_pr

