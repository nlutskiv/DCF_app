from stock import Stock
class Financials():
    """
    A class to handle financial calculations for a given stock ticker.
    """
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = Stock(ticker)


    def CAPM(self, R_f = 0.043, R_m=0.0932):
        """
        Calculate the Capital Asset Pricing Model (CAPM) for the stock.

        Parameters:
            R_f (float): Risk-free rate (default is 4.3%).
            R_m (float): Expected market return (default is 9.32%).

        Returns:
            float: The expected return based on CAPM.
        """ 
        beta = self.stock.get_beta()
        #print(R_f + beta * (R_m - R_f) )
        return R_f + beta * (R_m - R_f) 
        

    def WACC(self):
        """
        Calculate the Weighted Average Cost of Capital (WACC) for the stock.

        Parameters:
            None

        Returns:
            float: The WACC value.
        """
        tax = self.stock.get_tax()
        R_e = self.CAPM()
        D = self.stock.get_debt()
        E = self.stock.get_equity()
        R_d = self.stock.get_Rd()
        #print(f"R_e: {R_e}, D: {D}, E: {E}, R_d: {R_d}")
        #print(E / (D + E) * R_e + D / (D + E) * R_d * (1 - tax))
        
        return E / (D + E) * R_e + D / (D + E) * R_d * (1 - tax)
        

    def DCF(self, growth_rate=0.09, terminal_growth=0.025, discount_rate = None):
        """
        Calculate the Discounted Cash Flow (DCF) for the stock.
        Uses only last year's FCF, projects it forward with growth_rate for 5 years,
        then terminal_growth thereafter.
        """
        if discount_rate is None:
            discount_rate = self.WACC()
        elif discount_rate <= 0 or discount_rate >= 1:
            raise ValueError("Discount rate must be between 0 and 1.")
        
        #discount_rate = 0.095
        
        last_fcf = self.stock.get_FCF()
        #last_fcf = 13000000000.0
        print(f"Last FCF: {last_fcf}, Discount Rate: {discount_rate}, Growth Rate: {growth_rate}, Terminal Growth: {terminal_growth}")
        if not last_fcf or last_fcf == 0:
            return 0

        dcf_value = 0
        # Project next 5 years of FCF with growth_rate
        for i in range(1, 6):
            projected_fcf = last_fcf * ((1 + growth_rate) ** i)
            dcf_value += projected_fcf / ((1 + discount_rate) ** i)

        # Terminal value calculation
        terminal_fcf = last_fcf * ((1 + growth_rate) ** 5)
        terminal_value = (terminal_fcf * (1 + terminal_growth)) / (discount_rate - terminal_growth)
        dcf_value += terminal_value / ((1 + discount_rate) ** 5)

        return dcf_value
    
    def intrinsic_value(self):
        """
        Calculate the intrinsic value of the stock based on DCF.
        """
        dcf_value = self.DCF()
        shares_outstanding = self.stock.get_shares_outstanding()
        total_debt = self.stock.get_debt()
        net_debt = total_debt - self.stock.get_cash()
        if shares_outstanding > 0:
            return (dcf_value - net_debt)/ shares_outstanding
        else:
            return 0

