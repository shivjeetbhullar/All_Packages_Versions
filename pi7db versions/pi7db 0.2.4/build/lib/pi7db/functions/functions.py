import os,datetime,glob,random,pickle
from ..operators import *
from .. import cryptopidb as crdb
from ..status import error,success,info

def opendoc(file_path,key=None):
     if key is None:
       with open(f"{file_path}","rb") as f:return pickle.load(f)
     else:
       data = crdb.decrypt_file(file_path,key.encode())
       return pickle.loads(data)

def writedoc(file_path,data,key=None):
     if key is None:
      with open(f"{file_path}", "wb") as f:pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
      return True
     else:
      jsdata = pickle.dumps(data);crdb.encrypt_file(file_path,key.encode(),jsdata)
      return True

def extractfiles(path,Dic_data):
  remove_files,data_files = [f"{x}" for x in Dic_data['IGNORE']],[]
  for root, dirs, files in os.walk(path):
      for x in files:
        if x not in remove_files:data_files.append(f"{root}/{x}")
  return data_files

def nes_trash(d_dict, update_dict,keymatch=None):
    if isinstance(update_dict, set):
      for x in update_dict:d_dict.pop(x)
    else:
     for key, value in update_dict.items():
        if isinstance(value, dict) and key != "$where":
           d_dict[key] = nes_trash(d_dict.get(key, {}), value,keymatch)
        elif isinstance(value, set):
          for x in value:d_dict[key].pop(x)
        elif isinstance(value, list):
            for x in d_dict[key]:
               for xx in value:
                  if isinstance(xx, set):
                   for xxx in xx:x.pop(xxx)
                  elif "$where" and "$keys" in xx:
                     for xk in xx['$keys']:
                        if findDiff(xx['$where'],x):x.pop(xk)
                  else:nes_trash(x,xx)
            [d_dict[key].remove(x) for x in d_dict[key] if len(x) == 0]
    return d_dict

def trashbyfilter(dic_data,key_name,config):
 if len(dic_data):
  all_trash = []
  for x_path in dic_data:
   if x_path['cr_dc_path'] not in all_trash:all_trash.append(x_path['cr_dc_path'])
  for tr_path in all_trash:
    if not tr_path[-9:] == "pi7dbauto":
      if key_name is not None:
       tr_data = opendoc(tr_path,config['secret-key'])
       writedoc(tr_path,nes_trash(tr_data,key_name),config['secret-key'])
      else:os.remove(tr_path)
    else:
      v_data = opendoc(tr_path[:-9],config['secret-key'])
      if isinstance(v_data,list):
        for x_data in v_data:
          if x_data in dic_data:
            if key_name is not None:x_data=nes_trash(x_data,key_name)
            else:v_data.remove(x_data)
        writedoc(tr_path[:-9],v_data,config['secret-key'])
  return True

def nes_update(d_dict, update_dict,keymatch=None):
    for key, value in update_dict.items():
        if isinstance(value, dict) and key != "$where":           
           if increment_v in value:d_dict[key] = d_dict[key]+value[increment_v]
           elif decrement_v in value:d_dict[key] = d_dict[key]+value[decrement_v]
           else:d_dict[key] = nes_update(d_dict.get(key, {}), value,keymatch)
        elif isinstance(value, list):
            for x in d_dict[key]:
               for xx in value:            
                  if "$where" in xx:nes_update(x,xx,xx['$where'])
                  else:nes_update(x,xx)
        else:
           if key != "$where":
            if keymatch is None:d_dict[key] = value
            elif isinstance(keymatch,dict) and findDiff(keymatch,d_dict):d_dict[key] = value
    return d_dict

def updatebyfilter(dic_data,commands,config):
 if len(dic_data):
  all_update = []
  for x_path in dic_data:
   if x_path['cr_dc_path'] not in all_update:
     all_update.append(x_path['cr_dc_path'])
  for up_path in all_update:
    if not up_path[-9:] == "pi7dbauto":
      js_data=opendoc(up_path,config['secret-key'])
      js_data=nes_update(js_data,commands)
      print(js_data)
      writedoc(up_path,js_data,config['secret-key'])
    else:
      v_data = opendoc(up_path[:-9],config['secret-key'])
      if isinstance(v_data,list):
        for x_data in v_data:x_data=nes_update(x_data,commands) 
        writedoc(up_path[:-9],v_data,config['secret-key'])
  return success.s1(commands)

def appendjson(file_path,data,key=None):
     if key is None:
      l_data = opendoc(file_path,key)
      l_data.append(data)
      writedoc(file_path,l_data,key) 
     else:
      dic_data = json.loads(crdb.decrypt_file(file_path,key.encode()))
      dic_data.append(data)
      dic_data = json.dumps(dic_data);crdb.encrypt_file(file_path,key.encode(),dic_data)
     return True

def writenodoc(col_path,dic_data,config):
     path,files=f"{col_path}/{datetime.date.today().year}",[]
     if not os.path.exists(path):os.makedirs(path)
     for x in glob.glob(f"{path}/*"):
      if os.path.getsize(x) < config['doc_size']:files.append(x)
     if len(files):
       dic_data['cr_dc_path'] = f"{files[0]}pi7dbauto"
       appendjson(files[0],dic_data,config['secret-key'])
     else:
       cr_time = datetime.datetime.now().strftime("%Y%M%S%f")
       dic_data['cr_dc_path'] = f"{path}/{cr_time}{random.randint(10000, 99999)}pi7dbauto"
       writedoc(dic_data['cr_dc_path'][:-9],[dic_data],config['secret-key'])

def extract_kwargs(kw_dic,db_name):
     if 'IGNORE' in kw_dic:
        if isinstance(kw_dic["IGNORE"],str) or isinstance(kw_dic["IGNORE"],int):kw_dic["IGNORE"]=[kw_dic["IGNORE"],db_name]
        elif isinstance(kw_dic["IGNORE"],list):kw_dic["IGNORE"].append(db_name)
     else:kw_dic["IGNORE"]=[db_name]
     if len(kw_dic):
      if 'FIRST' in kw_dic:return {"f_a":None,"l_a":kw_dic['FIRST'],"IGNORE":kw_dic["IGNORE"]}
      if 'LAST' in kw_dic:return {"f_a":-kw_dic['LAST'],"l_a":None,"IGNORE":kw_dic["IGNORE"]}
      if 'FROM' in kw_dic:kw_dic["f_a"] = kw_dic['FROM']
      else:kw_dic["f_a"]=None
      if 'TO' in kw_dic:kw_dic["l_a"] = kw_dic['TO']
      else:kw_dic["l_a"]=None
      return kw_dic
     else:return {"f_a":None,"l_a":None,"IGNORE":kw_dic["IGNORE"]}

def check_GT_LT(d1,d2):
    if GT == d1[0] and isinstance(d1[1],int):
        if d1[1] < d2:return True
        else:return False
    elif LT == d1[0] and isinstance(d1[1],int):
        if d1[1] > d2:return True
        else:return False
    elif GET == d1[0] and isinstance(d1[1],int):
        if d1[1] <= d2:return True
        else:return False
    elif LET == d1[0] and isinstance(d1[1],int):
        if d1[1] >= d2:return True
        else:return False
    else:return False

def checkli_stin(l1,l2):
    return all(item in l2 for item in l1)

def string_filter(d1,d2):
    if d1[-2:] == '**' and d1[:2] == '**':
        if d1[:-2][2:] in d2:return True
    elif d1[-2:] == '**':
        if d2[:len(d1[:-2])] == d1[:-2]:return True
    elif d1[:2] == '**':
        if d2[-int(len(d1[2:])):] == d1[2:]:return True
    elif d1 == d2:return True
    else:return False

def checklist(l1,l2):
    for xx in enumerate(l1):
      for x in enumerate(l2):
        output = findDiff(l1[xx[0]],l2[x[0]])
        if output is True :break
    if output is None or output is True:return True 
    else:return False

boole = False
def findDiff(d1, d2):
    global boole
    for key in d1:
      if (key not in d2):pass
      else:
        if isinstance(d1[key],dict):
            if findDiff(d1[key],d2[key]) is False:return False
        elif type(d1[key]) is list:
          if all(isinstance(s, dict) for s in d1[key]):
            if checklist(d1[key],d2[key]) is False:boole = False;return False
          if all(isinstance(s, str) for s in d1[key]) or all(isinstance(i, int) for i in d1[key]):
              if checkli_stin(d1[key],d2[key]):boole = True
              else:boole = False;return False
        else:
          # <,> = Operators
          if isinstance(d1[key],tuple):
             if check_GT_LT(d1[key],d2[key]):boole = True
             else:boole = False;return False
          #STRING FILTER
          elif isinstance(d1[key],str):
            if string_filter(d1[key],d2[key]):boole = True
            else:boole = False;return False
          elif d1[key] == d2[key]:boole = True
          else:boole = False;return False
    
    return boole

def andfilter(command_tup,all_data):
  return [x for x in all_data if findDiff(command_tup,x) is True]

def create_coll(path):
  if not os.path.exists(path):os.mkdir(path)