# pi-audio-streamer-setup
A Cal Poly Computer Engineering Senior Project to develop a program that assists in a user configuring a Raspberry Pi as a digital audio streaming device.

Credits to dtcooper for creating Raspotify, which is what we use as the backbone to connect to Spotify. If you want to be able to set that up on your own, see here: 
https://github.com/dtcooper/raspotify

## Required Items

- Python 3.9+
- MicroSD Card (8GB or more)
- Raspberry Pi

We recommend the Raspberry Pi 3A+ as it has a headphone jack and full-size USB/HDMI, so that you don't need any adapters

NOTE: Any Raspberry Pi 1.X or Raspberry Pi Zero models are not supported due to limitations with Raspotify

## Configuration Instructions

### Flashing the SD Card

First you should download the Raspberry Pi Imager, from the official Raspberry Pi Foundation website
raspberrypi.com/software, then click on the version for the correct OS you want to download (This guide was written using MacOS).

<img width="563" alt="image" src="https://user-images.githubusercontent.com/46544653/170892407-daccff1f-4b86-4879-9ba3-e70c6c035afe.png">

After installing and launching the imager for the first time, it should look like this.

<img width="686" alt="image" src="https://user-images.githubusercontent.com/46544653/170892482-595edf7c-f230-4708-b982-45801dc5120e.png">

Click on "Choose OS", where you will then select "Raspberry Pi OS (other)" then "Raspberry Pi OS Lite (32-bit)"

<img width="687" alt="image" src="https://user-images.githubusercontent.com/46544653/170892542-693e2892-37f7-4050-9feb-07221d502a7c.png">

<img width="687" alt="image" src="https://user-images.githubusercontent.com/46544653/170892552-88fe3a6a-ac5d-42a6-80d4-b40f84680d2f.png">

Next, click on the gear in the bottom right of the GUI, where we will pre-configure some settings for the Raspberry Pi, which we will use in our script, as well as to setup connection to streaming services.

Enable the following settings:
NOTE: We are going to use the Raspberry Pi username/password later, so be sure to remember or write it down. You should choose something unique.

<img width="596" alt="image" src="https://user-images.githubusercontent.com/46544653/170892715-f3d308d4-cbe9-4c19-819e-479194d0a7f1.png">

<img width="592" alt="image" src="https://user-images.githubusercontent.com/46544653/172553310-39c5dc38-9140-4aab-adee-82204489f720.png">

Insert your MicroSD card into your computer (using a MicroSD card slot or MicroSD card reader)

Next, click on "Choose Storage" and select your MicroSD card from the list
- It's likely that it's the first item in the list

<img width="690" alt="image" src="https://user-images.githubusercontent.com/46544653/170892604-a65b72b4-4142-4024-b942-1f39d0f844fc.png">

Next, select the "Write" option, this should finish the setup of the Raspberry Pi OS. On MacOS you may be prompted to enter your password to give the application permission to write to the MicroSD card.

![image](https://user-images.githubusercontent.com/46544653/172557374-e5301686-2a12-4313-9244-374d6930a94d.png)

### Using our program

Once we have the OS set up, we can now move onto using the program to set up Raspotify
Initially, you will be greeted with this page in the program.

![image](https://user-images.githubusercontent.com/46544653/172558314-44516c29-7e01-47dc-bd75-361cc15733eb.png)

This page includes much of the same information that we just discussed, click "Next"

![image](https://user-images.githubusercontent.com/46544653/172561016-71ced175-6267-406b-9846-b4460362f557.png)

Remove the SD card from your computer, then plug it in to the Raspberry Pi and turn it on.

This page requires you to put in the same username and password that we saved away earlier as the profile for the pi.
We are going to use this information to connect to the pi.

You probably will not need to change the raspberrypi.local, however if you are having problems connecting to the Pi, then you can use the IP address of the Raspberry Pi.
(can be found in the devices list of your WiFi network page).

Click refresh, then click next when available. If the next button does not work, keep refreshing until it does (the Pi may take some time to turn on). If it does not work after
a considerable amount of tries, then try to find the IP address of the Pi (if you do not know how, there are articles that explain how to do so).

![image](https://user-images.githubusercontent.com/46544653/172565707-4412895d-b132-44cf-8ca5-bfaea4802ccd.png)

![image](https://user-images.githubusercontent.com/46544653/172566159-b6e5e989-e56f-425a-8b44-ca68b949bded.png)

This next screen is where some customization can be done, you can set both the device name and also the icon that will display in Spotify.

Click Next when you are satisfied with your options. At this point, the Raspberry Pi will be configured. This process can take multiple minutes, and it may appear as if the program has frozen. Be assured it is still working.

![image](https://user-images.githubusercontent.com/46544653/172577992-71bd173d-6947-4933-8582-e57cec5c6aea.png)

This next page will have a singular drop down, indicating which audio device on your Pi the program will configure itself to.
There will be a default option, which you can test by trying to cast to the device via Spotify, but if that audio device isn't playing sound, or it it's quiet, then choose a new audio device and click "Apply". If your device does not appear on the list, attempt to reconnect it and click "Refresh"

NOTE: This is what the device will look like in the casting section of the spotify web application (can be different for mobile).
![image](https://user-images.githubusercontent.com/46544653/172578454-49188505-d981-4a51-8bc8-7f3e8e85a1be.png)
