import ntplib
from time import ctime
c = ntplib.NTPClient()
response = c.request('127.0.0.1')
print(response.offset)
print(response.version)
print(ntplib.leap_to_text(response.leap))
print(ctime(response.tx_time))
print(response.root_dela)