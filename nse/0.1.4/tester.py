from nse import Nse

ns = Nse()


#print(ns.capture('OIL',1,new=True))

#print(ns.live('BAJAJ-AUTO'))  

#print(ns.linear('BAJAJ-AUTO',x='lastUpdateTime',y='buyQuantity2'))

#print(ns.archives)


#data = ns.archive('eqelm','05-03-2020')
#print(ns.calculator('OIL',55))
#fil = ns.csv_filter({"CLOSE":22.8},"OR",{"CLOSE":83.55},dict=data)

#print(ns.bar(fil,x='SYMBOL',y='OPEN'))
#print(fil)
#ns.csv_write('ds.csv',fil)


# assigning x and y coordinates  

#data = ns.load("OIL")

#s = {"data":[{"S":1,"a":2,"d":3},{"S":31,"a":24,"d":34}]}

#p = ns.pandas(s)
#print(ns.csv_write(data,write=False))


#print(ns.filter({"data":[{"lastPrice":'98**'}]}))

#print(ns.capture('niftyMidsml400Online',2))

# for x in ns.load()['data']:
#     try:
#      print(x['data'][0]['lastPrice'])
#     except:print(x)

# cok = {
# "Accept": "*/*",
# "Accept-Encoding": "gzip, deflate, br",
# "Connection": "keep-alive",
# "DNT": "1",
# "Host": "www1.nseindia.com",
# "Referer": "https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=HDFCBANK",
# "Sec-Fetch-Dest": "empty",
# "Sec-Fetch-Mode": "cors",
# "Sec-Fetch-Site": "same-origin",
# "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
# "X-Requested-With": "XMLHttpRequest"
# }

# from bs4 import BeautifulSoup 
# import requests

# url = "https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=HDFCBANK"
# url="https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/ajaxGetQuoteJSON.jsp?symbol=HDFCBANK&series=EQ"
# ua = "Mozilla/5.0 (Linux; Android 6.0.1; SM-G935S Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36"

# r = requests.get(url,headers=cok)


# #soup = BeautifulSoup(r.content, 'html.parser')

# #table = soup.find('ul', attrs = {'class':'stock'}) 
   
# print(r.text)