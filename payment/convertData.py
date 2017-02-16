#coding=utf-8
import datetime
class charToNumber:
    cdict={}
    gdict={}
    xdict={}
    def __init__(self):
        self.cdict={1:u'',2:u'拾',3:u'佰',4:u'仟'}
        self.xdict={1:u'元',2:u'万',3:u'亿',4:u'兆'} #数字标识符
        self.gdict={0:u'零',1:u'壹',2:u'贰',3:u'叁',4:u'肆',5:u'伍',6:u'陆',7:u'柒',8:u'捌',9:u'玖'}       

    def csplit(self,cdata): #拆分函数，将整数字符串拆分成[亿，万，仟]的list
        g=len(cdata)%4
        csdata=[]
        lx=len(cdata)-1
        if g>0:
            csdata.append(cdata[0:g])
        k=g
        while k<=lx:
            csdata.append(cdata[k:k+4])
            k+=4
        return csdata
    
    def cschange(self,cki): #对[亿，万，仟]的list中每个字符串分组进行大写化再合并
        lenki=len(cki)
        i=0
        lk=lenki
        chk=u''
        for i in range(lenki):
            if int(cki[i])==0:
                if i<lenki-1:
                    if int(cki[i+1])!=0:
                        chk=chk+self.gdict[int(cki[i])]                    
            else:
                chk=chk+self.gdict[int(cki[i])]+self.cdict[lk]
            lk-=1
        return chk
        
    def cwchange(self,data):
        cdata=str(data).split('.')
        
        cki=cdata[0]
        ckj=cdata[1]
        i=0
        chk=u''
        cski=self.csplit(cki) #分解字符数组[亿，万，仟]三组List:['0000','0000','0000']
        ikl=len(cski) #获取拆分后的List长度
        #大写合并
        for i in range(ikl):
            if self.cschange(cski[i])=='': #有可能一个字符串全是0的情况
                chk=chk+self.cschange(cski[i]) #此时不需要将数字标识符引入
            else:
                chk=chk+self.cschange(cski[i])+self.xdict[ikl-i] #合并：前字符串大写+当前字符串大写+标识符
        #处理小数部分
        lenkj=len(ckj)
        if lenkj==1: #若小数只有1位
            if int(ckj[0])==0: 
                chk=chk+u'整'
            else:
                chk=chk+self.gdict[int(ckj[0])]+u'角整'
        else: #若小数有两位的四种情况
            if int(ckj[0])==0 and int(ckj[1])!=0:
                chk=chk+u'零'+self.gdict[int(ckj[1])]+u'分'
            elif int(ckj[0])==0 and int(ckj[1])==0:
                chk=chk+u'整'
            elif int(ckj[0])!=0 and int(ckj[1])!=0:
                chk=chk+self.gdict[int(ckj[0])]+u'角'+self.gdict[int(ckj[1])]+u'分'
            else:
                chk=chk+self.gdict[int(ckj[0])]+u'角整'
        return chk

class ClosingDate():
        #计算货期
    def __init__(self,x):        
        self.transfer_finance=datetime.datetime.strptime(x['transfer_finance'], "%Y-%m-%d")  
        self.n=int(str(self.transfer_finance)[8:10])   #取当前日期的天数
        self.payment_date=int(x['payment_date'])
        self.closing_date=x['closing_date']

    def getClosingDate(self):        
        #payment_date是付款期限        
        #closing——date 是收票日
        if self.closing_date:
            closing_dateList=self.closing_date.split(u'、')
        else:
            closing_dateList=[]
        closing_dateListInt=[]
        for t in closing_dateList:
            try:
                closing_dateListInt.append(int(t))
            except:
                pass
        #获取最后付款时间        
        if closing_dateListInt:
            if closing_dateListInt[0]==0 and len(closing_dateListInt)==1:
                resultDate=self.transfer_finance+datetime.timedelta(days=self.payment_date)
            else:
                for t in closing_dateListInt:
                    if self.n>max(closing_dateListInt):
                        print("max")
                        resultDate=datetime.datetime(self.transfer_finance.year,self.transfer_finance.month+1,min(closing_dateListInt))+datetime.timedelta(days=self.payment_date)   
                        break
                    if t>self.n:
                        print(t-self.n)
                        resultDate=self.transfer_finance+datetime.timedelta(days=(t-self.n+self.payment_date))
                        break 
        else:
            resultDate=None

        return resultDate