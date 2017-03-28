import socket
#import importlib
#import config
#from Cython.Compiler.Errors import message
global config

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
            DL = dict([[l.split("=")[0],
                        ("=".join(l.split("=")[1:])).split("\"")[1] if "\"" in ("=".join(l.split("=")[1:])) else ("=".join(l.split("=")[1:]))] for
                       l in LLL])
            config.__dict__ = DL
    except Exception as e:
        print "[ERROR] Configurations parese incorrect"
        return False
    return True


#config = importlib.import_module("./config.py")
if __name__ == "__main__":
    parseConfig()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((config.ID_server, int(config.ID_port)))
    s.listen(int(config.ID_lsiten))
    ids=0
    with open(config.server_id, "w") as WF:
        while True:
            client, address = s.accept()
            client.settimeout(60)
            try:
                message=readlines(client).next()
                if message == config.ID_msg:
                    client.sendall(config.ID_ack + " " + str(ids)+"\n")
                    ids+=1
                    WF.write(str(ids)+"\n")
                    WF.flush()
                    print "Send ",ids,address
            except Exception as e:
                print e
