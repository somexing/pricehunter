#  coding:utf8
'''
用例1 获取所有最新降价的产品名称和价格
1 外部输入多个URL和匹配内容正则表达式，文件名 filename_all.cfg
2 读入之前保存的产品名称和价格 old_price_id_list
2 调用多线程获取每个URL得到网页内容并用对应的正则解出结果 new_price_id_list
3 对比 old_price_id_list，如果有降低则进行报告和记录


用例2 获取输入的某产品名称的最低价格
0 外部输入产品关键字  id
1 外部读入多个查询的URL和匹配内容正则表达式 filename_qry.cfg
2 读入之前保存的产品名称和价格 price_id_list
2.1 组合URL得到查询URL 
3 调用多线程获取每个URL得到网页内容并用对应的正则解出结果  new_price_id_list
4 对比  old_price_id_list，如果新访问到了最低的结果，如果有降低则进行报告和记录

类图
MT 
init() 传入urllist和relist
func() 传入url 和 re，返回2个list 





'''
import sys
import datetime
sys.path.append("../mymodule")
import bbs, re, func 

TEST_MODE = 1 



SITE = 'amazon'

def _print(value):
   printlock.acquire()
   if printmode == 1:
	    print(value )    
   if logmode  == 1:
      fplog.write(value+'\n')
   printlock.release()         
   return
   
   
class MT_2(object):
   def __init__(self, func, argsVector0, argsVector1, MAXTHREADS=15, queue_results=True):
                self._func = func
                self._lock = threading.Lock()
                self._nextArgs0  = iter(argsVector0).next                
                self._nextArgs1  = iter(argsVector1).next
                self._threadPool = [ threading.Thread(target = self._doFunc) for i in range (MAXTHREADS)]
                
                self._stopAllThread = False

                if queue_results:
                   self._queue = Queue.Queue()
                else:
                   self._queue = None
 
                   
   def _doFunc(self):  
          
                while (True):                
                	 if (self._stopAllThread):
                	    break
                   #get next passwd for crack   
                	 self._lock.acquire()
                	 try:
                	      try:
                	      	   arg0 = self._nextArgs0()
                	           arg1 = self._nextArgs1()
                	      except StopIteration:
                	           break
                	 finally:
                	      self._lock.release()   
                   
                	 rt = self._func(arg0, arg1)

                	 if (!rt ):
                	 	   _print("thread func run failed!Stop all threads !\n") 
                	 	   self._stopAllThread = True
                	 	   break
                     
             
               
   def get(self, *a, **kw):
                if self._queue is not None:
                    return self._queue.get(*a, **kw)
                else:
                    raise ValueError, 'Not queueing results'

   def start(self):
                for thread in self._threadPool:
                    time.sleep(0)  #give chance to other threads
                    thread.start()
                
   def join(self, timeout = None):
                for thread in self._threadPool:
                    thread.join(timeout)

	

def get_webpage_info(  url, re_str):              
              threadid = threading.currentThread().name
              for i in range( MAX_TRYCONNECT_NUM ):                   
                   try:                
                          timebefore =  time.time()  
                          rand = str(random.randint(1000,9999))                       
                         
                          if USE_PROXYFILE == 1:
                             PROXY_SERVER = proxyfilelines[random.randint(0,len(proxyfilelines)-1)].strip()  #strip /r/n     	  
                          
                          if USE_PROXY == 1:
                             conn = httplib.HTTPConnection(PROXY_SERVER, timeout = 1)
                          else:
                          	 conn = httplib.HTTPConnection(host, timeout = 1)
                          
                          conn.request( 'GET', url, '', headers =  header)
                          resp = conn.getresponse()
                          if resp.status != 200 and resp.status != 302:           
                               _print ("%s %s  arg0 = %s, arg1 = %s"%( resp.status, resp.reason , url, re_str))  
                               continue
                               
                          #print(resp.read())                #test    
                          #print(resp.read().decode('utf_8'))                #test    
                          content = resp.read().decode('utf_8')
                          #content = resp.read()                         
                          #_print(content.encode('gbk'))                #test    
                          

                          rematch = re.compile( re_str  )  #r''?      	
                          cont = rematch.findall(content)     
                          if len( cont ) == 0 :        
                         	   timecost =  time.time()-timebefore  
                         	   _print (" No Matching pattern ! arg0 = %s, arg1 = %s  , cost %s s"%(  url, re_str , timecost))  
                         	   break   
                          str1 = cont[0]  
                          str2 = cont[1]                                           
                   	      print ("Get it!! use %s. arg0 = %s, arg1 = %s  ,cost %s s"%(PROXY_SERVER,  url, re_str , timecost))                                                	   
                         	return True                                            
                   except  Exception, e:       
                          _print (" Exception :%s arg0 = %s, arg1 = %s"%(str(e), url, re_str ))                  	 	
                          continue
                          #if (str(e).find("10055") > -1) or (str(e).find("timed out") > -1):                              
                          #	  _print ("10055 timed out,try again  :  videoid %s, pwd %s"%(  videoid,  pwdToTry)) 
                          #	  continue
                          #else:
                          #	  break  
                          	  
              return  False
 
if __name__ == '__main__':
    if TEST_MODE ==1 :
      MAX_PAGE_IDX = 1  
    filename= 'lego'+datetime.date.today().strftime('%Y%m%d')+'.txt'
    fp = open(filename,'w')
    re1 = re.compile( str_topic_re )
    re2 = None #re.compile( str_content_re, re.S )
    re3 = re.compile( str_cleanhtml_re )
    re4 = re.compile( str_nextpage_re )
    relist = [re1, re2, re3, re4]
    amz = bbs.FixPageBBSCrawl()
    amz.init_argv(urllist,  relist,  fp , MAX_PAGE_IDX )
          
    urllist = [PAGE_URL_FIRST, PAGE_URL_prefix, PAGE_URL_postfix, TOPIC_URL_prefix, TOPIC_URL_postfix]  
        
    amz.OpenBBSTopicList1(urllist )

    fp.flush()
        
    fp.close() 
