//My 8mm camera mount has 4 parts:
//A base, on which the carriage can slide in and out toward the lens

//A carriage, which sits on top of the carriage and slides on rails made from lego wheel axles
//with a '+' shaped cross-section

//The camera mount, which sits snugly in the vertical slots of the carriage and can be adusted vertically
//The lens cover, holding the lens, and which can be fitted into the camera mount.


//This is the carriage. The small vertical slots in the rear are designed to fit a nut, 
//so that I could turn an m3 machine screw mounted in the base to fine-tune the focus.
//It didn't work very well, frankly, and I ended up just adjusting the carriage manually and 
//securing it in position with a piece of elastic.  
//If you're mechanically inclined, please share your improved design!

module channel() {
    union() {
        cube([4.8,60,1]);
        translate([1.2,0,0]) {cube([2.4,60,3.4]);}
        }
    }

difference() {
cube([35,60,5]);
translate([25.2,0,0]) {channel(); }
translate([5,0,0]) {channel(); }
}

difference(){
cube([35,7.75,30]);
translate([2.25,2,0]) {cube([30.5,3.75,30]);}
translate([5,0,0]) {cube([25,8,30]);}
}


difference(){
translate([11,50,5]){cube([13,6,10]);}
translate([12.5,52,5]){cube([10,2,10]);}
translate([15,50,8]){cube([5,6,7]);}
}