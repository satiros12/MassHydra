
#ID
ID="-1"
ID_server="192.168.93.135"
ID_port="5656"
ID_msg="GETID"
ID_ack="ACK"
ID_lsiten="1000"#Number of servers

#OWN EXECUTABLE
exe_brute="brute-hydra.exe"

#Server inforamtion
server="http://192.168.93.135:8080"
server_user="user.txt"
server_pass="pass.txt"
server_ips="ip.txt"
server_control="control.txt"
server_id="id.txt"
server_configurations="config.py"
server_output="output.txt"

control_updateTime="10.0"  #Every 10 second will se if control changed

#FTP
ftp_ip="192.168.93.135"
ftp_user="stan"
ftp_pass="satiros23"
ftp_dir="~/Documentos"

#GLOBAL
service_ssh="-t 10" #Additional options: -t, -w, -W
service_rdp="-t 10" #Separated by space

#HYDRA
exe_hydra="./attackers/hydra/hydra.exe"
hydra_output="output.txt"
hydra_local_threads="10"
hydra_thread_limit="50" #Limit of threads ssh+rdp
hydra_time_threadLimit="10"
hydra_time_finalWait="10.0"#Every 10 will review if hydra threads ended

