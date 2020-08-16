import io,zipfile,requests,random
from datetime import datetime
from .config import *
from bs4 import BeautifulSoup

def render_url(SYM):
    return f"https://www1.nseindia.com/live_market/dynaContent/live_watch/stock_watch/{SYM}StockWatch.json"

def render_cmp_url(SYM):
    return f"https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/ajaxGetQuoteJSON.jsp?symbol={SYM}&series=EQ"

def render_archive(name,date):
    return f"https://www1.nseindia.com/ArchieveSearch?h_filetype={name}&date={date}&section=EQ"

def render_calculator(self,U_A,SYS,QTY,T_TYPE="B",price=None,ts='EQ'):  
    if price is None:price = requests.get(f"https://www1.nseindia.com/live_market/dynaContent/live_watch/margincalc/marginCompanySearch.jsp?symbol={SYS}&series=EQ&method=getLTP",headers={'User-Agent':U_A}).text.strip()
    print(price)
    return f"https://www1.nseindia.com/live_market/dynaContent/live_watch/margincalc/calcMargin.jsp?segment=1&NoofRecords=1&flag=N&tradeSymbol={SYS}&tradeSeries={ts}&tradeQty={QTY}&tradePrice={price}&tradeType={T_TYPE}"

def checkdigit(num):
      if isinstance(num,str):
       num = num.replace(',','')
       if num.isdigit():return int(num)
       else:
        try:return float(num)
        except:return num
      else:return num

def extract_zip(url,U_A):
    if url[-4:] == '.csv':return [requests.get(url,headers={'User-Agent':random.choice(U_A)}).text]
    else:
     zipf = zipfile.ZipFile(io.BytesIO(requests.get(url,headers={'User-Agent':random.choice(U_A)},stream=True).content))
     return [zipf.read(x_num.filename).decode() for x_num in zipf.filelist if ".csv" in x_num.filename]

def checkdate(date):
   try:d_object = datetime.strptime(date, '%d-%m-%Y')
   except:raise Exception("Error! Make Sure Date Format Is DD-MM-YYYY")
   day = d_object.strftime("%A")
   if day == "Sunday" or day == "Saturday":raise Exception(f"Error! Stock Market Was Down On {date} Because of {day}.")

def extract_archive(self):
    try:
     if self.exists('archives',today=True):self.archives=self.read('config','archives','archives')['data']
     else:
      response = requests.get(urls.daily_archive,headers={'User-Agent':random.choice(self.read('User_Agents','firefox','UA')['data'])})
      soup = BeautifulSoup(response.text,"html.parser")
      self.archives={}
      for x in soup.findAll("option")[1:]:self.archives[x['value']] = x.text
      self.write('config','archives',{'archives':self.archives})
    except:pass
     