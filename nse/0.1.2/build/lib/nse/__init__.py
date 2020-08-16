import requests,json,time,os,random,pathlib,time
from bs4 import BeautifulSoup
from .config import *
from .functions import *
from pi7db import pi7db,csv
from matplotlib import pyplot as plt

class Nse(pi7db,csv):
  def __init__(self):
      pi7db.__init__(self,"DB", pathlib.Path(__file__).parent.absolute())
      self.brands=self.read('config','stock','brand')['data']
      extract_archive(self)

  def live(self,SYS): 
    try:
      data = json.loads(requests.get(render_cmp_url(SYS),headers={**self.read('config','cookies')['data'][0],'User-Agent':random.choice(self.read('User_Agents','firefox','UA')['data'])}).text)
      data.update(data.pop('data')[0])
      for x in data:data[x] = checkdigit(data[x])
      return data
    except:return {"Error":f"Make Sure {SYS} Is Avalible In NSE. For Check Some NSE Brands use print(self.brands)","Status":0}

  def archive(self,type_a,date):
    checkdate(date)
    if self.exists(date):return {"data":self.read('archives',f"{type_a}{date}")['data'][0]['values']}
    else:
      content,soup = [],BeautifulSoup(requests.get(render_archive(type_a,date),headers={**self.read('config','bhavcopy')['data'][0]['headers'],'User-Agent':random.choice(self.read('User_Agents','firefox','UA')['data'])}).text,"html.parser")
      try:
       for x_c in extract_zip(f"{urls.host}{soup.find('a')['href']}",self.read('User_Agents','firefox','UA')['data']):content.extend(self.csv_read(csv_str=x_c)['data'] )
      except:return error.e1(date)
      self.write('archives',f"{type_a}{date}",{"values":content})
      return {"data":content}
    
  def capture(self,SYS,minute,**kwargs):
    if "new" in kwargs and kwargs['new'] == True:self.trash(IGNORE_COLLECTION=['User_Agents','config'])
    timeout = time.time() + 60*minute
    if isinstance(SYS,str):SYS = [SYS]
    if isinstance(SYS,list):timeouts = short_timeouts
    while True:
     if time.time() > timeout:break
     else:
       for x in SYS:
        self.write(x,self.live(x))
        print(f"CAPTURING......{x}")
        time.sleep(random.choice(timeouts))
    return "Success!"
 
  def load(self,SYS=None):
    if SYS is None:return self.read(IGNORE=ignorefiles)
    else:return self.read(SYS)
  
  def calculator(self,SYS,QTY,T_TYPE="B",price=None,ts='EQ'):
    U_A = random.choice(self.read('User_Agents','firefox','UA')['data'])
    url = render_calculator(self,U_A,SYS,QTY,T_TYPE,price,ts)
    rs = requests.get(url,headers={'User-Agent':U_A}).text
    return rs

  def graphvalues(self,SYS,kwargs):
    if isinstance(SYS,dict):data,title = SYS['data'],"Stock"
    else:data,title=self.load(SYS)['data'],f"{SYS} Stock"
    if 'x' in kwargs and 'y' in kwargs:x,y = kwargs['x'],kwargs['y']
    else:x,y = 'lastUpdateTime','lastPrice'
    time=[];price=[]
    for x_d in data:
     time.append(x_d[x])
     price.append(x_d[y])
    return {"x":time,"y":price,'xt':x,'yt':y,'title':title}

  def bar(self,SYS=None,**kwargs):
    values = self.graphvalues(SYS,kwargs)
    plt.bar(values['x'],values['y'])
    plt.xlabel(values['xt'])  
    plt.ylabel(values['yt'])
    plt.title(values['title'])
    plt.show()

  def linear(self,SYS=None,**kwargs):
    values = self.graphvalues(SYS,kwargs)
    plt.plot(values['x'],values['y'], color='green')  
    plt.xlabel(values['xt'])  
    plt.ylabel(values['yt'])
    plt.title(values['title'])   
    plt.show()  
