import subprocess
import sys
import threading
import importlib

#ip = '192.168.160.188'
ip = 'raspberrypi.local'
script_file = 'script.sh'

def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def ssh_update():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())   # Replace with ignore???
    ssh.connect(ip,22,'pi', 'raspberry')

    ssh.exec_command('touch the_update_thread_ran') # Temporary proof this thread ran

    ssh.exec_command('echo "raspberry" | sudo -S apt update -y')
    ssh.exec_command('echo "raspberry" | sudo -S apt upgrade -y')

    ssh.close()


def ssh_script():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())   # Replace with ignore???
    ssh.connect(ip,22,'pi', 'raspberry')

    sftp = ssh.open_sftp()
    sftp.put(script_file, '/home/pi/script.sh') # Copy the script for the pi to run, that will do a lot of things
    sftp.close()

    ssh.exec_command('chmod +x /home/pi/script.sh') # Need the script to be executable
    ssh.exec_command('/home/pi/script.sh')  # Run Script
    
    ssh.close()


def main():
    print('Welcome to the setup program for the RaspberryPi Music Streamer!')
    print("Please don't continue unless you have already flashed Raspbian OS Lite on a >4GB MicroSD Card.")
    print('The easiest way to do this is to use the Raspberry Pi Imager software aavailable at raspberrypi.com/software\n')

    #mount /boot
    #copy wifi file, ssh file to /boot
    #modify files on /boot like cmdline.txt and config.txt (wifi file? or template first?)

    install('paramiko') # Paramiko may or may not be installed for the user, so, try to install it first
    globals()['paramiko'] = importlib.import_module('paramiko')

    #make a new thread and run ssh for the update file
    update_thread = threading.Thread(target=ssh_update)

    # Likely, we don't need a thread for the script to run in, just "main"
    #script_thread = threading.Thread(target=ssh_script)

    update_thread.start()   # Get the pi updating while we're continuing

    #get information from user, finish up script.sh, wait for update thread to finish
    print("Yo we're getting information from the user bro")

    update_thread.join()    # Wait for the update to finish before launching the script on the pi
    #script_thread.start()  # Likely unnecessary
    print('Yo the update is done!')
    
    # Modify the script

    ssh_script()    # Copy and launch the script, now that it has been fixed with the new information

    print('The installer has finished! @( * O * )@\nPlease note the Raspberry Pi may still be rebooting. It will be online shortly.')


if __name__ == '__main__':
    main()