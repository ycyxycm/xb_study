from datetime import datetime
from datetime import timedelta
from datetime import timezone


#返回参数时间+1天的时间
def get_addoneday_time(time):
    return (datetime.strptime(time,'%Y-%m-%d') + timedelta(days=1)).strftime("%Y-%m-%d")

# a=get_addoneday_time('2022-10-01')
# print(a)