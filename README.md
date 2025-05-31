# Dahua-RTSP-Saver

Overview
Dahua RTSP Saver is a tool designed to save IP camera video streams with possible AES encryption.

Features

    Saves IP camera video streams
    Supports AES encryption


Troubleshooting
FAQ
Q1: My video stream jumps forward regularly?
A1: This issue might occur if the frame rate of the Dahua IP camera exceeds the CPU's processing capacity. To resolve this:

    Lower the FPS or resolution of your IP camera stream
    Alternatively, set up multiple lines in the config file for each camera:

    - One line for live streaming (e.g., with high resolution)
    - Another line for saving (e.g., with lower resolution)
    - Each line spawns a new process, which can improve performance

Configuration Tips

    Each line in the config file spawns a new process
    Consider optimizing your config for better performance

License:
Creative Commons Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0) license

