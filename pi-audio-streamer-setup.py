import tkinter as tk
from tkinter import ttk
from tkinter import font
import webbrowser
import platform
import subprocess
import sys
import threading
import time

try:    # Paramiko is needed for SSH communication with the Raspberry Pi
    import paramiko
except:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'paramiko'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import paramiko

icon_types = ["Computer", "Tablet", "Smartphone", "Speaker", "TV", "Audio/Video Receiver", "Set-Top Box", "Audio Dongle", "Game Console", "Cast Audio", "Cast Video", "Automobile", "Smartwatch", "Chromebook", "CarThing", "HomeThing"]
icon_precise_names = ["computer", "tablet", "smartphone", "speaker", "tv", "avr", "stb", "audiodongle", "gameconsole", "castaudio", "castvideo", "automobile", "smartwatch", "chromebook", "carthing", "homething"]

root_window = tk.Tk()
root_window.title("Raspberry Pi Music Streamer Setup")

default_font = font.nametofont("TkDefaultFont")
default_font.configure(size=14)

home = ttk.Frame(root_window, padding=10)
instructions = ttk.Frame(root_window, padding=10)
options = ttk.Frame(root_window, padding=10)
installing = ttk.Frame(root_window, padding=10)
final = ttk.Frame(root_window, padding=10)
dir_result = None
ip_option = None
ip_addr = "raspberrypi.local"
device_name = "pi-audio"
device_icon = "audiodongle"
device_name_entry = None
instructions_next = None
pi_username_entry = None
pi_password_entry = None
pi_username = ""
pi_password = ""
audio_device_list = ["default"]
audio_device_selection = "default"
audio_device_space = None   # The blank frame to put a new audio device dropdown in
audio_device_selector = None    # The audio device dropdown itself
update_thread = None

# Utility Functions
def open_pi_page(event):
    webbrowser.open_new("https://www.raspberrypi.com/software/")

def ping_ip_addr(enable_button_flag=True):
    global ip_addr, instructions_next

    if platform.system().lower() == "windows":  # Windows pinging uses a different flag than UNIX
        flag = "-n"
    else:
        flag = "-c"

    command = ['ping', flag, '1', ip_addr]

    if subprocess.call(command) == 0:   # Allow re-enabling the next button if it's available on the network
        if instructions_next is not None and enable_button_flag == True:
            instructions_next['state'] = "normal"
        return True
    else:
        return False

def change_ip_addr():
    global ip_addr
    global ip_option
    
    ip_addr = ip_option.get()   # Get the new IP Address
    ping_ip_addr()  # Ping the new IP Address, and make "next" enabled if ping succeeds

def parseAudioDevices(str_t: str):
    returnList = []

    while (1):
        card_loc = str_t.find("card")
        if (card_loc == -1):
            break
        str_t = str_t[card_loc:]

        card_name_loc = str_t.find("[")
        card_name_end = str_t.find("]")
        name = str_t[card_name_loc+1:card_name_end]
        str_t = str_t[card_name_end:]

        returnList.append(name)
    return returnList

def refreshAudioDeviceList():
    global audio_device_selector, audio_device_list

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    ssh.connect(ip_addr, 22, pi_username, pi_password)
    stdin, stdout, stderr = ssh.exec_command("aplay -l")  # Returns a tuple, element 1 is stdout as a byte-string
    exit_status = stdout.channel.recv_exit_status() 
    if exit_status != 0:
        print("Error retrieving audio device list from Raspberry Pi: ", stderr.read().decode())
        exit(-1)

    audio_device_list = parseAudioDevices(stdout.read().decode())
    audio_device_selector["values"] = audio_device_list

def updatePi():
    global pi_username, pi_password

    print("Raspberry Pi Update Thread Launched")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    ssh.connect(ip_addr, 22, pi_username, pi_password)

    stdin, stdout, stderr = ssh.exec_command(f'echo "{pi_password}" | sudo -S apt update')
    exit_status = stdout.channel.recv_exit_status() 
    if exit_status != 0:
        print("Error executing apt update: ", stderr.read().decode())
        exit(-1)
    else:
        print(stdout.read().decode())
    
    stdin, stdout, stderr = ssh.exec_command(f'echo "{pi_password}" | sudo -S apt full-upgrade -y')
    exit_status = stdout.channel.recv_exit_status() 
    if exit_status != 0:
        print("Error executing apt full-upgrade: ", stderr.read().decode())
        exit(-1)
    else:
        print(stdout.read().decode())

    ssh.close()
    print("Raspberry Pi has finished updating")

def quit_confirmation():
    quit = tk.Toplevel(root_window)
    quit.title("Quit")

    # A Label widget to show in toplevel
    tk.Label(quit, text="Are you sure you want to quit?").pack(padx=20, pady=20)
    tk.Button(quit, text="Cancel", command=lambda: quit.destroy()).pack(anchor="s", side="left", padx=10, pady=10)
    tk.Button(quit, text="OK", command=lambda: exit(0)).pack(anchor="s", side="right", padx=10, pady=10)

def applyAudioDeviceSelection():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    ssh.connect(ip_addr, 22, pi_username, pi_password)

    index = audio_device_list.index(audio_device_selector.get())
    print(f"Audio device {index} selected: {audio_device_list[index]}")

    stdin, stdout, stderr = ssh.exec_command(f"echo '{pi_password}' | sudo -S sed -i -e '/defaults\.ctl\.card/ s/ .*/ {index}/' /usr/share/alsa/alsa.conf")
    exit_status = stdout.channel.recv_exit_status() 
    if exit_status != 0:
        print("Error in audio device change command 1: ", stderr.read().decode())
        exit(-1)

    stdin, stdout, stderr = ssh.exec_command(f"echo '{pi_password}' | sudo -S sed -i -e '/defaults\.pcm\.card/ s/ .*/ {index}/' /usr/share/alsa/alsa.conf")
    exit_status = stdout.channel.recv_exit_status() 
    if exit_status != 0:
        print("Error in audio device change command 2: ", stderr.read().decode())
        exit(-1)
    
    stdin, stdout, stderr = ssh.exec_command(f"amixer -c {index} set $(amixer -c {index} scontrols | cut -d \\' -f2) 100%")
    exit_status = stdout.channel.recv_exit_status() 
    if exit_status != 0:
        print("Error setting audio device volume to 100%: ", stderr.read().decode())
        exit(-1)
    else:
        print(stdout.read().decode())

    ssh.close()

# Next Button Functions
def gotoInstructions():
    home.destroy()
    instructions.pack()

def gotoOptions():
    global root_window, pi_username_entry, pi_password_entry, pi_username, pi_password, update_thread, instructions, options

    if ping_ip_addr() == False:
        print("The Pi is not responding to pings, will not proceed")
        return

    pi_username = pi_username_entry.get()
    pi_password = pi_password_entry.get()

    if pi_username == "":
        print("No username given")
        return

    update_thread = threading.Thread(target=updatePi)
    update_thread.start()

    instructions.destroy()
    options.pack()

def runScript():
    global options, installing, final, device_name

    device_name = device_name_entry.get()
    if device_name == "":
        print("No device name given")
        return

    options.destroy()
    installing.pack()

    # Wait on the update thread to finish
    update_thread.join()

    # Run the raspotify installation over paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    print(pi_username, pi_password)
    ssh.connect(ip_addr, 22, pi_username, pi_password)

    stdin, stdout, stderr = ssh.exec_command(f"echo '{pi_password}' | sudo -S apt-get -y install curl && curl -sL https://dtcooper.github.io/raspotify/install.sh | sh")
    exit_status = stdout.channel.recv_exit_status() 
    if exit_status != 0:
        print("Error executing raspotify installation script: ", stderr.read().decode())
        exit(-1)
    else:
        print(stdout.read().decode())

    stdin, stdout, stderr = ssh.exec_command(f'echo "{pi_password}" | sudo sed -i \'s/Environment=LIBRESPOT_NAME="%N (%H)"/Environment=LIBRESPOT_NAME="{device_name}"\\nEnvironment=LIBRESPOT_DEVICE_TYPE="{icon_precise_names[icon_types.index(device_icon.get())]}"/\' /usr/lib/systemd/system/raspotify.service\n')
    exit_status = stdout.channel.recv_exit_status() 
    if exit_status != 0:
        print("Error editing raspotify config file: ", stderr.read().decode())
        exit(-1)
    
    ssh.exec_command(f"echo '{pi_password}' | sudo -S reboot")
    ssh.close()

    print("Setup Finished, the Raspberry Pi will now reboot. The next page will be available after it is back online.")
    time.sleep(5)   # Wait 5 seconds for the Pi to stop responding to pings
    while ping_ip_addr(False) == False:
        print("not yet, waiting 5s before trying again")
        time.sleep(5)

    time.sleep(5)
    
    refreshAudioDeviceList()

    installing.destroy()
    final.pack()
    
# Page Defenitions
def homePage():
    ttk.Label(home, text="Welcome to the setup program for the RaspberryPi Music Streamer!", font=("", 20, "bold")).pack(anchor="n", padx=10, pady=10)
    ttk.Label(home, text="Please first install Raspberry Pi OS Lite on a MicroSD card for use with your Raspberry Pi").pack()
    ttk.Label(home, text="This can be done easily using the Raspberry Pi Foundation's Imager, available for download here:").pack()
    link_pp = ttk.Label(home, text="raspberrypi.com/software", foreground="dodger blue", cursor="hand")
    link_pp.pack(padx=10, pady=10)
    link_pp.bind("<Button-1>", open_pi_page)
    ttk.Label(home, text="Please note the following configuration options before pressing \"Write\" in the Raspberry Pi Imager").pack(pady=20)
    ttk.Label(home, text="For the Operating System, Raspberry Pi OS Lite (32-bit) is under \"Raspberry Pi OS (other)\".").pack(anchor="w", padx=10, pady=5)
    ttk.Label(home, text="For Storage, choose the MicroSD Card you wish to use (must be connected to your computer).").pack(anchor="w", padx=10, pady=5)
    ttk.Label(home, text="Press the gear in the bottom right corner for Advanced Configuration Options, and configure the following:").pack(anchor="w", padx=10, pady=5)
    ttk.Label(home, text="If you're setting up multiple devices, select \"Set hostname\" and use a unique hostname for each device.").pack(anchor="w", padx=30)
    ttk.Label(home, text="Check \"Enable SSH\", with \"Use password authentication\" as the selected option.").pack(anchor="w", padx=30)
    ttk.Label(home, text="Check \"Set username and password\", and choose a username and password. This will be needed again on the next page of this application.").pack(anchor="w", padx=30)
    ttk.Label(home, text="Check \"Configure wireless LAN\", and enter your WiFi Information. This computer must be on the same network as the Raspberry Pi.").pack(anchor="w", padx=30)
    ttk.Label(home, text="Uncheck \"Eject media when finished\".").pack(anchor="w", padx=30)
    ttk.Label(home, text="Once you've installed Raspberry Pi OS Lite on a MicroSD card as described above, hit \"Next\"").pack(pady=20)

    ttk.Button(home, text="Quit", command=lambda: quit_confirmation()).pack(anchor="s", side="left", padx=10, pady=10)
    ttk.Button(home, text="Next", command=lambda: gotoInstructions()).pack(anchor="s", side="right", padx=10, pady=10)

def piInstructionsPage():
    global instructions, ip_addr, ip_option, pi_password_entry, pi_username_entry, instructions_next

    ttk.Label(instructions, text="Booting the Raspberry Pi the 1st Time").pack()
    ttk.Label(instructions, text="Please remove the MicroSD card from your computer, insert it into your Raspberry Pi, and plug the Raspberry Pi in to power.").pack(pady=10)
    ttk.Label(instructions, text="For this application to be able to connect to the Raspberry Pi, it will need the username and password you previously gave it.").pack(pady=10)

    username_frame = ttk.Frame(instructions)
    ttk.Label(username_frame, text="Raspberry Pi Username").pack(side="left", padx=10, pady=5)
    pi_username_entry = ttk.Entry(username_frame, textvariable=pi_username)
    pi_username_entry.pack(side="right", padx=10, pady=5)
    username_frame.pack(fill="x")

    password_frame = ttk.Frame(instructions)
    ttk.Label(password_frame, text="Raspberry Pi Password").pack(side="left", padx=10, pady=5)
    pi_password_entry = ttk.Entry(password_frame, textvariable=pi_password)
    pi_password_entry.pack(side="right", padx=10, pady=5)
    password_frame.pack(fill="x")

    ttk.Label(instructions, text="\nThe next button will become available when the Raspberry Pi has been detected by this computer.").pack()
    ttk.Label(instructions, text="If the next button does not become available after some time, ensure the IP Address is correct.").pack()

    ip_addr_frame = ttk.Frame(instructions)
    ttk.Label(ip_addr_frame, text="Raspberry Pi's hostname or IP Address (default is raspberrypi.local)").pack(side="left", padx=10, pady=10)
    ip_option = ttk.Entry(ip_addr_frame)
    ip_option.insert(0, ip_addr)
    ip_option.pack(side="right", padx=10, pady=10)
    ip_addr_frame.pack()

    ttk.Button(instructions, text="Quit", command=lambda: quit_confirmation()).pack(anchor="s", side="left", padx=10, pady=10)
    instructions_next = ttk.Button(instructions, text="Next", command=lambda: gotoOptions(), state="disabled")
    instructions_next.pack(anchor="s", side="right", padx=10, pady=10)
    ttk.Button(instructions, text="Refresh", command=lambda: change_ip_addr()).pack(anchor="s", side="right", padx=10, pady=10)

def additionalOptionsPage():
    global options, device_name, device_icon, device_name_entry

    ttk.Label(options, text="The Raspberry Pi is Currently Updating...").pack()

    ttk.Label(options, text="Additional Configuration Options").pack()

    device_name_frame = ttk.Frame(options)
    ttk.Label(device_name_frame, text="Device Name").pack(side="left", padx=10, pady=10)
    device_name_entry = ttk.Entry(device_name_frame, textvariable=device_name)
    device_name_entry.insert(0, device_name)
    device_name_entry.pack(side="right", padx=10, pady=10)
    device_name_frame.pack(fill="x")

    icon_frame = ttk.Frame(options)
    ttk.Label(icon_frame, text="Device Icon").pack(side="left", padx=10, pady=10)
    device_icon = tk.StringVar(icon_frame)
    device_icon.set(icon_types[icon_types.index("Audio Dongle")])
    icon_field = ttk.Combobox(icon_frame, textvariable=device_icon, values=icon_types)
    icon_field.pack(side="right", padx=10, pady=10)
    icon_frame.pack(fill="x")

    ttk.Label(options, text="When you hit next, the setup will be run on the Raspberry Pi. This process can take a while.").pack(padx=10, pady=10)
    ttk.Label(options, text="This setup application may appear as though it has frozen, which is normal behavior.").pack(padx=10, pady=10)
    ttk.Label(options, text="On the final screen, you'll have an opportunity to choose the audio device you wish to use.").pack(padx=10, pady=10)

    ttk.Button(options, text="Quit", command=lambda: quit_confirmation()).pack(anchor="s", side="left", padx=10, pady=10)
    ttk.Button(options, text="Next", command=lambda: runScript()).pack(anchor="s", side="right", padx=10, pady=10)

def installingPage():
    # Currently, at least on my machine, while this page would be nice to have up while the Pi is updating, it doesn't load
    # until after the entire setup is finished. At that point, it then moves on immediately to the final page.
    
    ttk.Label(installing, text="The Raspberry Pi will finish updating and proceed to install and configure the necessary packages.").pack(padx=50, pady=50)

def finalPage():
    global audio_device_space, audio_device_list, audio_device_selector

    ttk.Label(final, text="Audio Device Selection").pack()

    ttk.Label(final, text="At this point, your Raspberry Pi should have all necessary packages installed and configured!").pack(padx=10, pady=10)
    ttk.Label(final, text="Go ahead and try casting music to the Raspberry Pi. If you can't hear anything, the default audio device may be incorrect.").pack(padx=10)
    ttk.Label(final, text="If necessary, you can change the audio device below. You may need to re-cast to the Raspberry Pi after clicking \"Apply\".").pack(padx=10)

    audio_device_space = ttk.Frame(final)
    ttk.Label(audio_device_space, text="Audio Device").grid(row=0, column=0, padx=10)#.pack(side="left", padx=10, pady=10)
    audio_device_selection = tk.StringVar(audio_device_space)
    audio_device_selection.set(audio_device_list[0])
    audio_device_selector = ttk.Combobox(audio_device_space, textvariable=audio_device_selection, values=audio_device_list)
    audio_device_selector.grid(row=0, column=1, padx=10)#.pack(padx=10, pady=10)
    ttk.Button(audio_device_space, text="Apply", command=lambda: applyAudioDeviceSelection()).grid(row=0, column=2, padx=10)#.pack(side="right", padx=10, pady=10)
    audio_device_space.pack(padx=10, pady=20)

    ttk.Label(final, text="If the desired device does not appear in the list, press refresh.").pack(padx=10, pady=10)

    ttk.Button(final, text="Finish", command=lambda: exit(0)).pack(anchor="s", side="right", padx=10, pady=10)
    ttk.Button(final, text="Refresh", command=lambda: exit(0)).pack(anchor="s", side="right", padx=10, pady=10)

# Main
def main():
    # Create all pages
    homePage()
    piInstructionsPage()
    additionalOptionsPage()
    installingPage()
    finalPage()

    # The home page should be "loaded" first (made visible)
    home.pack()

    root_window.mainloop()

if __name__ == "__main__":
    main()
