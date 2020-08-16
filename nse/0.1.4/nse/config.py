timeouts = [5,9,7,8]
short_timeouts = [4,2,3]

class urls:
  Stock_values = "https://www1.nseindia.com/live_market/dynaContent/live_watch/equities_stock_watch.htm"
  host = "https://www1.nseindia.com"
  daily_archive = "https://www1.nseindia.com/products/content/equities/equities/archieve_eq.htm"

ignorefiles = ['firefox','stock','cookies']
ignore = ['firefox','stock','cookies']

class error:
  def e1(date):
    raise Exception({"Error":f"Maybe There Is National Holiday On {date} OR File Is Not Avalible on NSE.","ststus":0})