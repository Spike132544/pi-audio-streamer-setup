# pi-audio-streamer
A Cal Poly Computer Engineering Senior Project to develop a program that assists in a user configuring a Raspberry Pi as a digital audio streaming device.

Credits to dtcooper for creating raspotify, which is what we use as the backbone to connect to Spotify. If you want to be able to set that up on your own, see here: 
https://github.com/dtcooper/raspotify

## Configuration Instructions

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


<img width="596" alt="image" src="https://user-images.githubusercontent.com/46544653/170892715-f3d308d4-cbe9-4c19-819e-479194d0a7f1.png">

Insert your SD card into your computer (using an SD card slot on and select

Next, click on "Choose Storage" and select

<img width="690" alt="image" src="https://user-images.githubusercontent.com/46544653/170892604-a65b72b4-4142-4024-b942-1f39d0f844fc.png">

