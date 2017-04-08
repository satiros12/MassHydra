import sys, psutil, subprocess, time
from PyQt4 import QtGui
global config

def kill(proc_pid):
    try:
        process = psutil.Process(proc_pid)
        for proc in process.children(recursive=True):
            proc.kill()
        process.kill()
    except Exception as e:
        print "Can't kill process",proc_pid,e


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


class BruteGui(QtGui.QMainWindow):
    def __init__(self):
        super(BruteGui, self).__init__()
        self.initUI()
        self.id_server = "./id_server.exe"
        self.id_process = None

    def initUI(self):
        #Layout
        widget = QtGui.QWidget(self)
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        #Buttons
        controlButtons = ["Load","Id","Start","Stop","Log"]
        self.Buttons = []
        for ib,cb in zip(range(len(controlButtons)),controlButtons):
            self.Buttons.append(QtGui.QPushButton(cb))
            self.Buttons[-1].clicked.connect(self.buttonPushed)
            #if cb == "Log":
            #    self.Buttons[-1].setCheckable(True)
            grid.addWidget(self.Buttons[-1],ib,3)

        #Lines
        inputLines = ["REFRESH:","ID IP:","HTTP IP:","FTP IP:","FTP USER:","FTP PASS:","FTP DIRECTORY:","SSH OPTS:","RDP OPTS:","MAX THREADS:"]
        inputLinesV = ["control_updateTime", "ID_server", "server", "ftp_ip", "ftp_user", "ftp_pass",
                      "ftp_dir", "service_ssh", "service_rdp", "hydra_thread_limit"]
        self.LableLines = []
        for ib, cb, vcb in zip(range(len(inputLines)), inputLines, inputLinesV):
            QLE = QtGui.QLineEdit()
            QLE.setText(config.__dict__[vcb])
            self.LableLines.append([vcb,(QtGui.QLabel(cb),QLE)])
            grid.addWidget(self.LableLines[-1][1][0], ib,0)
            grid.addWidget(self.LableLines[-1][1][1], ib,1)
        self.LableLines = dict(self.LableLines)
        widget.setLayout(grid)
        self.setCentralWidget(widget)
        self.statusBar()

        self.setGeometry(500, 500, 500, 300)
        self.setWindowTitle('Brute Massive Force : SSH+RDP ')
        self.show()

    def buttonPushed(self):
        global config
        sender = self.sender()
        ts = sender.text()
        #["Load", "Id", "Start", "Stop", "Log"]
        if(ts == "Load"):
            for l in self.LableLines:
                config.__dict__[l] = str(self.LableLines[l][1].text())
            with open("./config.py","w") as WF:
                for c in config.__dict__:
                    WF.write(str(c) + "=\"" + config.__dict__[c] + "\"\n")
            with open(config.server_control, "w") as WF:
                WF.write("load")
        elif(ts== "Id"):
            if self.id_process != None:
                kill(self.id_process.pid)
            self.id_process = subprocess.Popen([self.id_server])
            with open(config.server_control, "w") as WF:
                WF.write("id")
        elif(ts == "Start"):
            with open(config.server_control, "w") as WF:
                WF.write("start")
        elif(ts == "Stop"):
            with open(config.server_control, "w") as WF:
                WF.write("stop")
        elif (ts == "Log"):
            with open(config.server_control, "w") as WF:
                WF.write("log")
        time.sleep(float(config.control_updateTime))
        self.statusBar().showMessage(sender.text())

    def closeEvent(self, event):
        if self.id_process != None:
            kill(self.id_process.pid)

def main():
    parseConfig()
    #t_id_server = threading.Thread(target=id_server)
    app = QtGui.QApplication(sys.argv)
    ex = BruteGui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()