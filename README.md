# rpi-film-capture
A project to perform frame-by-frame capture of 8mm and 16mm films using a raspberry pi &amp; camera, and a modified movie projector.

Design Basics:
* Film transport is performed by a repurposed projector. (8mm, Super8, or 16mm)
* Raspberry Pi acts as a headless server, controlling the camera and driving the projector via a stepper motor.
* Python 'client' program runs on a higher-power computer on the same network. It sends control commands to the RPi server, and perform processing on images as they are captured.  All user

Optimizations for Speed:
* Sending captured images over the network rather than saving them locally reduces time between frames.
* Multithreading used on both client and server to reduce I/O delays.
* All computationally demanding processing is performed by the (faster) client.
* Can capture via the Pi Camera stills port (slower) or can blend captures from the video port for increased speed.

Optimizations for Quality:
* Performs exposure bracketing on frames and combine them, to capture a much higher dynamic range than the Pi Camera normally permits.
* Full control over Pi Camera's settings, some of which can be changed during capture.

Optimizations for Ease of Use:
* 'Setup Mode' allows for precise adjustment of camera before starting capture.
* Save settings between uses or for individual reels
* Real-time display of captured images
* 'Smart capture' features to adjust to dramatic lighting changes (under development)
* Entire system can be moved easily from one projector to another to change film gauges.

See the [wiki](./wiki/Home.md) for complete documentation, including a manual, wiring diagrams, and hardware selection tips for your own project.
