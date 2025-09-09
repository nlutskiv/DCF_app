from stock import Stock
from finance import Financials

class Company():
    def __init__(self, ticker):
        """
        Initialize the Company with a ticker symbol.
        """
        self.ticker = ticker
        self.stock = Stock(ticker=ticker)
        self.finance = Financials(ticker=ticker)
