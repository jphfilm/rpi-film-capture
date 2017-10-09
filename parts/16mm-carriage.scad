//A very basic mount camera mount for the 16mm projector.
//There was, luckily, a flat, horizontal section of metal casing slightly below the lens.
//The mount is primarily held to this metal with a magnet (which sits in the derpression in the base.
//I also put a bit of double-sided tape between the mount and the base, just to add a bit of tackiness so it doesn't slide around.
//I use a rubber band to secure the camera to the mount
TOTAL_WIDTH=30;
BORDER_WIDTH=3;
BORDER_HEIGHT=30;

difference() {
    cube([TOTAL_WIDTH,40,4]);       //Base of mount
    translate([15,20,1.6]) cylinder(r=9.5, h=5); //Cutout for magnet
    }

//Presumably I had something in mind when I designed this upside down and flipped it around.
//But I couldn't tell you what it was.  Sorry.
translate([TOTAL_WIDTH,0,33]){   
    rotate([180,0,-90]){
        difference(){
            //Vertical Surface for Camera Mount
            translate([-BORDER_WIDTH,0,0]){ cube([BORDER_WIDTH,TOTAL_WIDTH,BORDER_HEIGHT]);}

            //Camera Opening
            translate([-BORDER_WIDTH-1,10,8]){cube([9,9,9]);} //The hole through the mount
            translate([-BORDER_WIDTH-1,7,17]){cube([3,12,10]);} //Cutout below lens for connector between sensor chip and PCB
            translate([-BORDER_WIDTH-1,2,2]){cube([BORDER_WIDTH/2,25,25]);} //Camera Seating area
        }
    }
}