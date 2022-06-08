# pi-audio-streamer
A Cal Poly Computer Engineering Senior Project to develop a program that assists in a user configuring a Raspberry Pi as a digital audio streaming device.

Credits to dtcooper for creating raspotify, which is what we use as the backbone to connect to Spotify. If you want to be able to set that up on your own, see here: 
https://github.com/dtcooper/raspotify

## Required Hardware

- Python 3.9+
- MicroSD Card (8GB or more)
- Raspberry Pi

We recommend the Raspberry Pi 3A+ as it has a headphone jack and full-size USB/HDMI, so that we don't need any adapters

NOTE: Raspberry Pi One or Raspberry Pi Zero are not supported

## Configuration Instructions

### Flashing the SD Card

First you want to download the raspberry pi imager, from the official website
raspberrypi.com/software, then click on the version for the correct OS you want to download (I am using macOS so I will download that version).

<img width="563" alt="image" src="https://user-images.githubusercontent.com/46544653/170892407-daccff1f-4b86-4879-9ba3-e70c6c035afe.png">

After installing and launching the imager for the first time, it should look like this.

<img width="686" alt="image" src="https://user-images.githubusercontent.com/46544653/170892482-595edf7c-f230-4708-b982-45801dc5120e.png">

Click on "Choose OS", where you will then select "Raspberry Pi OS (other)" then "Raspberry Pi OS Lite (32-bit)"

<img width="687" alt="image" src="https://user-images.githubusercontent.com/46544653/170892542-693e2892-37f7-4050-9feb-07221d502a7c.png">

<img width="687" alt="image" src="https://user-images.githubusercontent.com/46544653/170892552-88fe3a6a-ac5d-42a6-80d4-b40f84680d2f.png">

Next, click on the gear in the bottom left of the GUI, where we will pre-configure some settings for the Raspberry Pi, which we will use in our script, as well as to setup connection to streaming services.

Enable the following settings:
NOTE: We are going to use the raspberry pi username/password later, so be sure to remember or write it down.

<img width="596" alt="image" src="https://user-images.githubusercontent.com/46544653/170892715-f3d308d4-cbe9-4c19-819e-479194d0a7f1.png">

<img width="592" alt="image" src="https://user-images.githubusercontent.com/46544653/172553310-39c5dc38-9140-4aab-adee-82204489f720.png">

Insert your SD card into your computer (using an SD card slot or SD card reader)

Next, click on "Choose Storage" and select your SD card from the list
- It should be the first item in the list

<img width="690" alt="image" src="https://user-images.githubusercontent.com/46544653/170892604-a65b72b4-4142-4024-b942-1f39d0f844fc.png">

Next, select the "Write" option, this should finish the setup of the Raspberry Pi OS.

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

You probably will not need to change the raspberrypi.local, however if you are having problems connecting to the Pi, then you can use the ip address of the Raspberry Pi.
(can be found in the devices list of your wi-fi network page).

Click refresh, then click next. If the next button does not work keep refreshing until you can (the Pi is turning on). If it does not work after
a considerable amount of tries, then try to find the ip address of the Pi (if you do not know how, there are articles that explain how to do so.

![image](https://user-images.githubusercontent.com/46544653/172565707-4412895d-b132-44cf-8ca5-bfaea4802ccd.png)

![image](https://user-images.githubusercontent.com/46544653/172566159-b6e5e989-e56f-425a-8b44-ca68b949bded.png)

This next screen is where some customization can be done, you can set both the device name and also the icon that will display in Spotify.

Click Next when you are satisfied with your options.

![image](https://user-images.githubusercontent.com/46544653/172577992-71bd173d-6947-4933-8582-e57cec5c6aea.png)

This next page will have a singular drop down, indicating which audio device on your Pi the program will configure itself to.
There will be a default option, which you can test by trying to cast to the device via Spotify, but if that audio device isn't playing sound, then choose a new audio device and click refresh.

NOTE: This is what the device will look like in the casting section of the spotify web application (can be different for mobile).
![image](https://user-images.githubusercontent.com/46544653/172578454-49188505-d981-4a51-8bc8-7f3e8e85a1be.png)
