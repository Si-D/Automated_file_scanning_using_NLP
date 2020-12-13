import datetime
from dateutil.relativedelta import relativedelta

x = datetime.datetime(2020,5,19) + relativedelta(years=+1) + relativedelta(days=+1)
y = x.strftime('%d/%m/%Y')
print(y)