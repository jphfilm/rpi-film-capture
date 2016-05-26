# rpi-film-capture
A project to capture 8mm and 16mm films using a raspberry pi &amp; camera, and a modified movie projector.



Background:
This project was born out of an attempt to capture over 130 rolls of 8mm, Super8, and 16mm films shot by an ancestor from the 1930s through the 1970s.  
Why frame-by-frame?
With a projector, and a digital SLR, and the proper lenses it is fairly straightforward to directly project the film into the camera at speed.  This approach has some significant drawbacks, however:
It is extremely difficult to precisely control the speed of most projectors, so as the projector speed 'drifts' over time, it will cause the captured video to consist of many frames that are actually a blending of two frames.
This may not look bad when projecting, but it makes such a movie almost impossible to improve with post-processing.  For one, changing the speed in an editing program will accentuate the 'blended' frames.  Also, many digital dust/dirt-removal tools require a frame-by-frame capture, because if a speck of dirt appears twice on multiple frames it will be treated as part of the film and not removed.
For a high-quality capture, frame-by-frame is absolutely essential.


Goals:
Use inexpensive, easily available equipment
Involve as little fabrication and building as possible, ideally avoiding custom-made parts
Capture film as quickly as possible

Alternate approaches:
jas8mm also uses a raspberry pi and a built-from-scratch transport mechanism.   I went with modifying a projector because (a) I already had one and (b) my film was all in reasonably good condition, with few torn sprockets.


Parts/Equipment List:

Projector: See discussion
Two wired Ethernet connectors on your network. (This could theoretically work over WiFi, but has not been tested, and could be much slower.)
A 'client' computer with Python, connected to your wired network:  Tested system is on Ubuntu, but should work on OSX or Windows with the proper libraries installed.  
Raspberry Pi: Tested system is on a RPi 3, but an original model B should work, if more slowly.
Stepper Motor: Bipolar NEMA 17
Stepper Motor Driver: A4988 or DRV____
Relay

Misc components:
Reed switch
Magnet
Momentary switch
47microFarad or larger capacitor
Several LEDs for use as indicator lights
220ohm resistors


Selecting the Projector:
Many old projectors will be suitable, even those in poor repair.  You'll need to modify it to the point where it is no longer working. If you're careful you may be able to return it to a working state.  We're not interested in the original lamp, lens, or motor and will actually be removing them.   We DO care about the following features:
An accessible manual film-advance wheel: This is fairly common on old projectors, and it's what we'll be attaching our motor to.  One revolution advances the frame a single step.
Working film advance path and gate:  This is the whole reason we're using an old projector instead of building something ourselves; the design and precision of this mechanism solves a LOT of problems for us. 
Working or repairable takeup reel mechanism:  This is usually driven by the same mechanics via gears or a belt that's designed to slip to avoid placing too much tension on the takeup reel.
Accessible space at least one side of the film.  On _either_ the lamp side or the lens side, you'll want extra space to get the camera in quite close to the film.  Our light source will be on the other, but it doesn't matter which.
Avoid 'auto-load' projectors: They make it very difficult to remove the film partway through a reel.
Dual-gauge projectors may save you some time but tend to have finicky film advance mechanisms.
Within these limits, smaller and simpler is often better.

Projector modifications:
This will require some creativity, depending upon your setup.  I've now modded 3 different projectors (8mm, super8, 16mm for this project, and though each presented their own challenges, they all worked.
Remove or disconnect the existing motor, lamp, and lens.
Remove the shutter: Most projectors have a 3-bladed shutter which blocks the light during projection 3 times per frame, so that flicker is imperceptible.  This will be in our way, so it needs to come off.
Find a way of attaching a motor to the film advance wheel.  Depending on the projector, you may need to modify the housing a bit to get at this.  I used a section of fuel hose and some small hose clamps, but YMMV.
(Optional) File open the gate so that the full frame is exposed.  Most projectors hide the edges of the film, and you'll probably want to see it all.  You can crop it in post-production.
Mount a magnet and a magnetic (reed) switch somewhere to the frame advance mechanism, so that the magnet closes the switch once per revolution, ideally just after the projector has finished advancing the film.  

