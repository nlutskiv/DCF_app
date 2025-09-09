import yfinance as yf
import pandas as pd

class Stock():
    def __init__(self, ticker):
        self.ticker = ticker



    def get_equity(self):
        try:
            stock = yf.Ticker(self.ticker)
            info = stock.info
            return info.get('marketCap', 0)  # Default to 0 if market cap is not available
        except Exception as e:
            print(f"Error getting equity for {self.ticker}: {e}")
            return 0
        

    def get_debt(self):
        try:
            stock = yf.Ticker(self.ticker)
            info = stock.info
            return info.get('totalDebt', 0)  # Returns 0 if not available
        except Exception as e:
            print(f"Error getting debt for {self.ticker}: {e}")
            return 0

    
    def get_beta(self):
        try:
            stock = yf.Ticker(self.ticker)
            info = stock.info
            return info.get('beta', 0)  # Returns 0 if beta is not available
        except Exception as e:
            print(f"Error getting beta for {self.ticker}: {e}")
            return 0
        

    def get_tax(self):
        """
        Estimate tax rate as Income Tax Expense / Income Before Tax.
        Returns 0 if data is missing.
        """
        try:
            stock = yf.Ticker(self.ticker)
            fin = stock.financials
            if 'Income Tax Expense' in fin.index and 'Income Before Tax' in fin.index:
                tax_expense = fin.loc['Income Tax Expense'].iloc[0]
                income_before_tax = fin.loc['Income Before Tax'].iloc[0]
                if income_before_tax != 0:
                    return abs(tax_expense) / income_before_tax
            return 0
        except Exception as e:
            print(f"Error getting tax for {self.ticker}: {e}")
            return 0


    def get_Rd(self):
        """
        Estimate cost of debt (Rd) as Interest Expense / Total Debt.
        Returns 0 if data is missing.
        """
        try:
            stock = yf.Ticker(self.ticker)
            info = stock.info
            interest_expense = info.get('interestExpense', 0)
            total_debt = info.get('totalDebt', 0)
            # Try financials if interestExpense is missing or zero
            if interest_expense == 0:
                fin = stock.financials
                if 'Interest Expense' in fin.index:
                    interest_expense = fin.loc['Interest Expense'].iloc[0]
                    #print(f"Interest Expense from financials: {interest_expense}")
            #print(f"Interest Expense: {interest_expense}, Total Debt: {total_debt}")
            if total_debt > 0 and interest_expense != 0:
                return abs(interest_expense) / total_debt
            else:
                print(f"Invalid Rd calculation for {self.ticker}: Interest Expense = {interest_expense}, Total Debt = {total_debt}")
                return 0
        except Exception as e:
            print(f"Error getting Rd for {self.ticker}: {e}")
            return 0
        
    def get_FCF(self):
        """
        Find Free Cash Flow (FCF) as Operating Cash Flow - Capital Expenditures,
        or use 'Free Cash Flow' if available.
        Returns 0 if data is missing.
        """
        try:
            stock = yf.Ticker(self.ticker)
            cashflow = stock.cashflow
            #print("Cashflow index:", cashflow.index)  # Debug: see available rows
            # Try to get Free Cash Flow directly
            if 'Free Cash Flow' in cashflow.index:
                #print(cashflow.loc['Free Cash Flow'].iloc[0])
                return cashflow.loc['Free Cash Flow'].iloc[0]
            # Otherwise, calculate from components
            if 'Total Cash From Operating Activities' in cashflow.index and 'Capital Expenditures' in cashflow.index:
                operating_cash_flow = cashflow.loc['Total Cash From Operating Activities'].iloc[0]
                capital_expenditures = cashflow.loc['Capital Expenditures'].iloc[0]
                return operating_cash_flow - capital_expenditures
            else:
                print(f"Free Cash Flow components not found for {self.ticker}")
                return 0
        except Exception as e:
            print(f"Error getting FCF for {self.ticker}: {e}")
            return 0


    def get_shares_outstanding(self):
        """
        Get the number of shares outstanding for the stock.
        Returns 0 if data is missing.
        """
        try:
            stock = yf.Ticker(self.ticker)
            info = stock.info
            return info.get('sharesOutstanding', 0)  # Default to 0 if not available
        except Exception as e:
            print(f"Error getting shares outstanding for {self.ticker}: {e}")
            return 0
        
        
    def get_cash(self):
        """
        Get the cash and cash equivalents for the stock.
        Tries multiple sources: info['cash'], info['cashAndCashEquivalents'], then balance sheet.
        Returns 0 if data is missing.
        """
        try:
            stock = yf.Ticker(self.ticker)
            info = stock.info
            # Try both possible keys in info
            cash = info.get('cash', 0)
            if not cash:
                cash = info.get('cashAndCashEquivalents', 0)
            if cash:
                return cash
            # Try balance sheet as fallback
            bs = stock.balance_sheet
            for label in ['Cash And Cash Equivalents', 'Cash']:
                if label in bs.index:
                    return bs.loc[label].iloc[0]
            return 0
        except Exception as e:
            print(f"Error getting cash for {self.ticker}: {e}")
            return 0


s = Stock("UNH")
#print(s.latest_annual_fcf())  # Example usage
#df_val.to_csv("value_candidates.csv", index=False)
#print(s.get_equity("UNH"))  # Example usage

#print(s.get_shares_outstanding())  # Example usage