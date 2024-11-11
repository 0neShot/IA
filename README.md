# Welcome to Interdisziplinäres Arbeiten (IA)!

Hi! This project is about controlling a robot with a PS5 Dualsense controller for testing, combined with a line follower algorithm.
You can easily add commands for further needs off your project.

# Requirements

- PyDualsense: https://github.com/flok/pydualsense
- Keyboard: https://thepythoncode.com/article/control-keyboard-python
- CustomTkinter: https://github.com/TomSchimansky/CustomTkinter

PyDualsense only works with **Windows or Linux!**

# QuickStart 

TLDR: Edit config, upload files, connect to network and controller, start programm and drive 

## Step 1

 - Edit the Config.py to fit your model configuration (sensors, motorpins, …). 
 - Enter your network credentials (hotspot or lokal network)!

## Step 2

 - Upload config.py, main.py, picommunicationPc.py, motorControl.py and PID.py to the raspberry pico.

## Final Step

 - Wait for the pico to connect to your network. When it is connected the led will turn green.
 - Start LocalPC.py. The controller will vibrate if the connection is
   successful and a GUI will open

# Documentation

Documentation will follow
