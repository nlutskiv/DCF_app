from company import Company


c = Company("ADBE")

value = c.finance.intrinsic_value()
debt = c.stock.get_debt()
cash = c.stock.get_cash()
print(value)
print(debt)