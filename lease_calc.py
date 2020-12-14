import datetime
from datetime import date
from datetime import timedelta
def getDate():
  date_entry = input()
  day, month, year = map(int, date_entry.split('-'))
  return datetime.date(year, month, day)
da = getDate()
yrs=int(input())
def addYears(d, years):
    try:
#Return same day of the current year        
        return d.replace(year = d.year + years)
    except ValueError:
#If not same day, it will return other, i.e.  February 29 to March 1 etc.        
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))
string=str(addYears(da,yrs))
from datetime import datetime
oldformat = string
datetimeobject = datetime.strptime(oldformat,'%Y-%m-%d')
newformat = datetimeobject.strftime('%d-%m-%Y')
print(newformat)
