import ntplib
from time import ctime
c = ntplib.NTPClient()
response = c.request('127.0.0.1')
print(ctime(response.tx_time))