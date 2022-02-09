import subprocess
import sys
import os
import threading
import re

# Since paramiko may not be imported, try to import it or install it if it isn't installed, then import it.
try:
    import paramiko
except:
    import importlib
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'paramiko'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import paramiko
    # Apparently, a regular import works actually
    # globals()['paramiko'] = importlib.import_module('paramiko')

ip = '192.168.160.188'
#ip = 'raspberrypi.local'
script_file = 'script.sh'

# This function may not be necessary if only paramiko is being 'live-installed'
# def install(package):    
#     subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
#     globals()[package] = importlib.import_module(package)

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


def directory(drive_letter):
    path = drive_letter + os.sep

    print(path)


def wpa_supplicant_update(country, SSID, password):
    wpa_template =  open('resources/wpa_supplicant.template', 'r+')
    text = wpa_template.read()
    text = re.sub('<UserCountry>', country, text)
    text = re.sub('<UserSSID>', SSID, text)
    text = re.sub('<UserPassword>', password, text)
    wpa_template.close()

    wpa_conf = open('resources/wpa_supplicant.conf', 'x')
    wpa_conf.write(text)
    wpa_conf.close()


def config_txt_update(filepath):
    config_txt = open(filepath, 'a')
    config_txt.write('\n')
    config_txt.write('dtoverlay=dwc2')
    config_txt.close()


def cmdline_txt_update(filepath):
    config_txt = open(filepath, 'a')
    config_txt.write(' modules-load=dwc2,g_ether')
    config_txt.close()


def main():
    print(directory('G:'))
    print("Welcome to the setup program for the RaspberryPi Music Streamer!")
    print("Please don't continue unless you have already flashed Raspbian OS Lite on a >4GB MicroSD Card.")
    print('The easiest way to do this is to use the Raspberry Pi Imager software aavailable at raspberrypi.com/software\n')
    print('You can input CTRL-C to stop the execution of this program at any time.\n')

    print("First, we'll need your WiFi information to get the Raspberry Pi updating before we continue.")
    # ssid = input('WiFi SSID: ')
    # wifipass = input('WiFi Password: ')

    # Needs better storage of password and some input trimming
    countrycode = input('Enter 2-character country code (e.g. US, GB, ...): ')
    ssid = input('Enter Wi-Fi Name (SSID): ')
    wifipass = input('Enter Wi-Fi Password: ')

    print('\nGreat! Now please re-insert your microSD card, making sure that it is visible to your computer.')
    # Use of input instead of print to have the program wait for a keypress.
    input('Press any key to continue.')

    # Detection of where /boot is, and mapping to it

    wpa_supplicant_update(countrycode, ssid, wifipass)
    config_txt_update("./resources/config.txt")
    cmdline_txt_update("./resources/cmdline.txt")

    #mount /boot
    #copy wifi file, ssh file to /boot
    #modify files on /boot like cmdline.txt and config.txt (wifi file? or template first?)

    #make a new thread and run ssh for the update file
    update_thread = threading.Thread(target=ssh_update)

    # Likely, we don't need a thread for the script to run in, just "main"
    #script_thread = threading.Thread(target=ssh_script)

    update_thread.start()   # Get the pi updating while we're continuing

    # Get User Input and Modify script.sh accordingly
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