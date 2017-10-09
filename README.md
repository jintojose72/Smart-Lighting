# Smart-Lighting

Project Name: Smart-Lighting
Description:
This project consists of two files namely project.py and mobile.py.

1. Project Folder :
a) project.py consists of code which will subscribe to a topic and also publish to the same topic when a button is pressed. On pressing the button, the led is turned on or off based on its previous state and a message with the current state of led light is published. It also has the code which receives the messages that are being published to topic and if the message is from the remote system, it takes the message and takes appropriate action based on the received message, whether to turn on or turn off the led light.

b) mobile.py consists of the code which will subscribe to same topic and also publish when a command is sent. In this file, the remote system tracks the current state of led light and will process the command whether to turn on or turn off the led. If a 'on' command is entered, the led is turned on and if an 'off' command is received, the led is turned off. As it is subscibed to the topic it receives the messages of the current state of led continuously and display's the state on the output console.

Run the project.py in raspberry-pi and run mobile.py in any remote system.

2. Output folder: 

This folder has output of both raspberry-pi and remote system at each state being processed.

3. Certificates folder: 

This folder has the certificates, private and public keys.
