Manual about the Brute Hydra Attack System:

Important files:
brute-hydra.exe  : The attacker program which generates and controls all Hydra SSH and RDP attacks
brute_client.exe : Client that communicates with the server, and runs btute-hydra.exe when "start" is set
id_server.exe : The server that gives ID to each attacker.

SERVER CONFIGURATION:
1. Setup HTTP server, in which main directory must be the next files:

ip.txt : List of IP's, an IP in each line.
pass.txt : List of passwords, an password in each line.
user.txt : List of users, an user in each line.
config.py : configuration file, few varaibles for different system configurations.
    Most important variables to set:
        ID_server="192.168.93.135" -> Set it with your server IP
        server="http://192.168.93.135:8080" -> Set ti with your HTTP server IP and PORT
        control_updateTime="2.0" -> Period for control referesh. In this case, each 2 seconds it will look at the remote control file and apply commands. (don't set ti too small, can produce errors)
        ftp_ip="192.168.93.135" -> Set the IP addres of your FTP server
        ftp_user="stan" -> User name of your FTP servers account
        ftp_pass="sant" -> Password of your FTP servers account
        ftp_dir="~/Documentos" -> Directory in which you want to receive the output of attackers (founded users and password)
        service_ssh="-t 10" -> Additional SSH Hydra attack configurations (look at attackers\hydra\hydra.exe -h)
        service_rdp="-t 10" -> Additional RDP Hydra attack configurations (look at attackers\hydra\hydra.exe -h)
        hydra_thread_limit="1000" -> Number of simultaneous hydra attacks (may be your system don't supor so much attacks)
control.txt : In this file you will set commands (only one word) to control all your attackers simultaneously. Every attacker will look here every "control_updateTime" seconds.
    Each comand is only one word in this file. Each comand is only applied once, if you want to repeat a command, put any other command or a non command word (as "none") and your command again then.
    Comands:
        id : Attackers will get the ID from the id_server.
        load : Attackers will downlaod ip.txt, pass.txt, user.txt and config.py from the server. Remmember to take your id again (config.py will erase the previous ID).
        start : Attackers will start their attacks, running brutal-hydra.exe and writting outputs to the brutal.log (which you can get with "log" command)
        stop : Attackers will end their brutal-htdra.exe process.
        log : Attackers will send by FTP to the server their logs in format as {ID}_brutal.log (as 0_brutal.log for the process with ID 0).
                --> This is a special command, don't use it if you want to reuse another command. This command is executed each "control_updateTime" seconds, to refresh the log files.

 2. Run the HTTP server in the server machine.
 3. Start the FTP server in the server machine.
 4. Write "none" into the control.txt -> To start without any initial command
 5. Start brute_client.exe in each attacker machine (zombie machines).
        --> It starts without paramters and controlled only by the contol.txt file. This program don't writte in any log.
 6. Write "load" into control.txt -> Let the attackers download all configuration files.
        * Wait "control_updateTime" second before the next step.
 7. Start the id_server.exe in the server machine.
 8. Write "id" into control.txt -> Let the attackers to get theirs IDs
    * Wait "control_updateTime" second before the next step.
 9. Write "start" into control.txt -> Let the attackers begin their attacks.
    --> All founded "users" and "password" that worked, will be written through FTP as {ID}_output.txt file (for the proces with ID as 0, this file will be 0_output.txt)
    * Wait "control_updateTime" second before the next step.
 10. Writte "log" into control.txt -> Now all attackers will send their logs to your FTP directory. You will be able to see how the attacks are going.
            --> Each log will be written en to the {ID}_brute.log file (for the process with ID 0, this file will be 0_brute.log)
 11. If you want, you can stop all attacks with the command "stop".
 12. You can restart the attack, or modify the config.py, ip.txt, users.txt or/and pass.txt file and reload all configurations with "load" command.
        ** Remember, every time you use the command "load", then stop the "id_server.exe", start it again "id_server.exe" and use the command "id" again.
            Only then use the "start" command. All attackers need to restart their ID.

 NOTE 1 : Don't put attacker IP into ip.txt file, it can make your attacker to frieze for some time.
 NOTE 2 : To quit id_server.rxr of brute_client.exe, can press Ctrl+C in the terminal.
