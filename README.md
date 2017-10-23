# rpi-film-capture

<img align="right" src="images/pifilm-setup.png">
A project to perform frame-by-frame capture of 8mm and 16mm films using a raspberry pi, the pi camera, and a modified movie projector. 
<img src="images/super8setup.jpg" width="480">

**UPDATE 10/23/2017: Several significant updates are coming soon, which may be worth waiting for if you're just startingout. If you're looking into this project, you may want to wait check back in a week or so, when I expect these to be available.  These include:
* Port to Python 3 and Qt5 (currently uses python 2.7 and qt4)
* Redesigned UI to reduce need for frequent switching between panels
* Executables for linux, to avoid the complicated install/compilation process currently necessary (hopefully OSX & windows coming later)
* Flat-field correction and distortion correction to compensate for effects introduced by non-stock lenses
* Improved documentation

**Update: If you're implementing this and want suggestions/advice from other users, consider joining the [google group](https://groups.google.com/forum/#!forum/rpi-film-capture)

Design:
* Film transport is via a repurposed projector (8mm, Super8, or 16mm), driven by a stepper motor. 
* Raspberry Pi acts as a headless server, controlling the camera, driving the motor, and streaming captured images over a network to a more powerful client.
* Python 'client' program runs on a higher-power computer on the same network. It sends control commands to the Pi server, and performs processing on images as they are captured.

Optimizations for Speed:
* Streaming images over network reduces I/O delay between frames, compared to saving them locally.
* Multithreading on both client and server further reduces I/O delays.
* All computationally demanding processing (esp. image fusion; see below) is performed by the (faster) client.
* Can capture via the Pi Camera's (slower) stills port, or can blend captures from the video port for increased speed.
* Practical per-frame capture times range from 1.6s/frame for 3-exposure bracketing from still port, down to .5s/frame for single-exposure captures from video port.

Optimizations for Quality:
<img  align="right" src="images/pifilm-advanced.png">
* Performs exposure bracketing on frames and combine them, to capture a much higher dynamic range than the Pi Camera normally permits.
* Full control over Pi Camera's settings, some of which may be changed mid-capture.
* Some simple histogram adjustment tools can do some processing on captured images before saving.

Optimizations for Usability:
* 'Setup Mode' allows for precise adjustment of camera before starting capture.
<img  align="right"src="images/pifilm-capture.png">
* Near-real-time view of captured images.
* Save/load settings, e.g. for different film types or projector setups.
* 'Smart capture' features to adjust to dramatic lighting changes (under development)
* Entire system can be moved from one projector to another to change film gauges.

See the [wiki](https://github.com/jphfilm/rpi-film-capture/wiki)(still under construction) for complete documentation, including a manual, wiring diagrams, and hardware selection tips for your own project.

Demonstration video, samples, and comparison w/ direct capture at speed available on my [YouTube channel](https://www.youtube.com/channel/UCQi6WqZvf4OT9eOhWeVfKMg).
Many more capture examples on my [Vimeo channel](https://vimeo.com/jphfilm)

