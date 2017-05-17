__author__ = 'xuxin'

def telnetdo(HOST=None, USER=None, PASS=None, COMMAND=None):  #定义一个函数, 这将要用它会很容易      5
    import telnetlib, sys
    msg = []
    if   not   HOST:                           #如果没有给出所要的资料，则要求用户输入
        try:
            HOST   = sys.argv[1]                 #记得吧, 序列是从 0开始数的，而sys.argv[0]会是你程式的名字     10
            USER   = sys.argv[2]
            PASS   = sys.argv[3]
            COMMAND   = sys.argv[4]
        except:
            print   "Usage: telnetdo.py host user pass 'command'"
            return msg.append(['Debug   mesages:\n'])             #这个用来存起所有从主机传回的讯息, 作除错时很有用
        tn   = telnetlib.Telnet()                  #准备一个 telnet 连线的实体
        try:
            tn.open(HOST)                           #连接端绑定到主机 HOST  去
        except:
            print   "Cannot open host"
            return  msg.append(tn.expect(['login:'],5))        #等待主机传回含有 'login:'字符的讯息，等候时限为 5秒
            # 27   tn.write(USER+'\n')                        #向主机送出字串 USER   + '\n'，如 USER  是    28
        # 'pcheung' 则等于 'pcheung\n'    29   if   PASS:                                 #就像是在键盘打入一样。     30      msg.append(tn.expect(['Password:'],5))  #如果有 password  要打的话就送出密码字串，     31      tn.write(PASS+'\n')                     #但首先要等主机传回含有 'Password:'字样的讯息     32     33   msg.append(tn.expect([USER],5))            #因为通常登入后主机会显示出登入者名称，我们在主机回应中找这     34                                              #样的字符，如有的话则代表登入成功了     35   tn.write(COMMAND+'\n')                     #向主机发出指令     36   msg.append(tn.expect(['%'],5))             #等 5秒，如果程式完成了一般我们会收到     37                                              # shell prompt  吧，假设为 '%'    38   tn.close()                                 #关闭连线     39   del   tn    40   return   msg[len(msg)-1][2]                #把收到的讯息通通传回去。     41                                              #(注意 msg  中第 2个元素才是真的讯息，     42                                              #其他是附加资讯。     43     44 if __name__   == '__main__'                  #这是 python  常用的技巧：如果 telnetdo.py 程式    45                                              #是从 command prompt    46                                              #引发的话则 __name__  的内容为 __main__，相反    47                                              #如果是从别的程式用 import telnetdo  的话则    48                                              # __name__  会变成 'telnetdo'    49   print   telnetdo()                         #这样写的好处是从此 telnetdo  会成为你的扩展    50                                              #模组，你可以在别的程式中     51                                               #用telnetdo.telnetdo(HOST,USER,PASS,COMMAND)来调用它！
