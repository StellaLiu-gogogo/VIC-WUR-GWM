import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta

def prepare_dates(current_date):
    startyear, startmonth, startday = current_date.year, current_date.month, current_date.day
    _, lastday = calendar.monthrange(startyear, startmonth)  # to get the last day of the month

    statedate = datetime(startyear, startmonth, lastday) # to get the state as a datetime object
    #stateyear, statemonth, stateday = statedate.year, statedate.month, statedate.day #to specify config file
    stateyear, statemonth, stateday = (current_date + relativedelta(months=1)).year, (current_date + relativedelta(months=1)).month, 1

    init_date = current_date 
    #init_date = current_date - relativedelta(days = 1)
    #init_datestr = init_date.strftime('%Y%m%d')  #for generating statefile name  
    init_datestr = current_date.strftime('%Y%m%d')  #for generating statefile name  

    endyear, endmonth, endday = (current_date + relativedelta(months=1)).year, (current_date + relativedelta(months=1)).month, 1

    return startyear, startmonth, startday, endyear, endmonth, endday, stateyear, statemonth, stateday, init_date, init_datestr