import subprocess
import sys
import threading
#import importlib

ip = '192.168.99.188'
update_file = 'update.sh'
script_file = 'script.sh'

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def ssh_update():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())   # Replace with ignore???
    ssh.connect(ip,22,'pi', 'raspberry')

    ssh.exec_command("touch the_update_thread_ran")

    ssh.exec_command('echo "raspberry" | sudo -S apt update -y')
    ssh.exec_command('echo "raspberry" | sudo -S apt upgrade -y')

    # stdin, stdout, stderr = ssh.exec_command('touch test')

    # stdin, stdout, stderr = ssh.exec_command('echo "raspberry" | sudo -S apt update -y')
    # stdin, stdout, stderr = ssh.exec_command('echo "raspberry" | sudo -S apt upgrade -y')
    
    # Junk?????????
    # alldata = ""
    # while not stdout.channel.exit_status_ready():
    # solo_line = ""        
    # # Print stdout data when available
    # if stdout.channel.recv_ready():
    #     # Retrieve the first 1024 bytes
    #     solo_line = stdout.channel.recv(1024) 
    #     alldata += solo_line
    # if(cmp(solo_line,'uec> ') ==0 ):    #Change Conditionals to your code here  
    #     if num_of_input == 0 :
    #     data_buffer = ""    
    #     for cmd in commandList :
    #     #print cmd
    #     stdin.channel.send(cmd)        # send input commmand 1
    #     num_of_input += 1
    #     if num_of_input == 1 :
    #     stdin.channel.send('q \n')      # send input commmand 2 , in my code is exit the interactive session, the connect will close.
    #     num_of_input += 1 
    # print alldata
    ssh.close() 


    # subprocess.run(['sshpass', '-p', 'raspberry', 'scp', '-o', 'StrictHostKeyChecking=no', update_file, 'pi@{ip}:~'.format(ip=ip)])
    # p = subprocess.Popen(['sshpass', '-p', 'raspberry', 'ssh', 'pi@{ip}'.format(ip=ip), '-o', 'StrictHostKeyChecking=no', '-f', './{file}'.format(file=update_file)], stdout=subprocess.PIPE)
    # p.wait()


def ssh_script():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())   # Replace with ignore???
    ssh.connect(ip,22,'pi', 'raspberry')

    sftp = ssh.open_sftp()
    sftp.put("~", "script.sh")
    sftp.close()    #does this close the ssh connection too?

    ssh.exec_command("~/script.sh")

    ssh.close()

    # subprocess.run(['sshpass', '-p', 'raspberry', 'scp', '-o', 'StrictHostKeyChecking=no', script_file, 'pi@{ip}:~'.format(ip=ip)])
    # p = subprocess.Popen(['sshpass', '-p', 'raspberry', 'ssh', 'pi@{ip}'.format(ip=ip), '-o', 'StrictHostKeyChecking=no', '-f', './{file}'.format(file=script_file)], stdout=subprocess.PIPE)

    # for line in p.stdout:
    #     print(line)

    # p.wait()

def main():
    print("Welcome to the setup program for the RaspberryPi Music Streamer!")
    print("Please don't continue unless you have already flashed Raspbian OS Lite on a >4GB MicroSD Card.")
    print("The easiest way to do this is to use the Raspberry Pi Imager software aavailable at raspberrypi.com/software\n")

    # sshpass provides an easy way to respond to a password prompt, so, that must be installed. Will ask user for their password
    # print("Our program requires a supporting package sshpass")
    # subprocess.run(['sudo', 'apt', 'install', 'sshpass', '-y'])

    try:
        import paramiko
    except: # Install and then import paramiko
        import importlib
        install('paramiko')
        globals()['paramiko'] = importlib.import_module('paramiko')

    #make a new thread and run ssh for the update file
    update_thread = threading.Thread(target=ssh_update)
    #script_thread = threading.Thread(target=ssh_script)

    update_thread.start()

    #get information from user, finish up script.sh, wait for update thread to finish
    print("Yo we're getting information from the user bro")

    update_thread.join()    # Wait for the update to finish before launching the script on the pi
    #script_thread.start()
    print("Yo the update is done!")
    #ssh_script()

    print("The installer has finished! @( * O * )@\nPlease note the Raspberry Pi may still be rebooting. It will be online shortly.")


if __name__ == "__main__":
    main()