//See 8mm-carriage.scad for documentation

module channel() {
    mirror ([0,0,1]) {
    union() {
        cube([5.4,60,1]);
        translate([1.6,0,0]) {cube([2.2,60,3.4]);}
        }
    }
}


difference() {
cube([35,60,6]);
translate([25.2,0,6]) {channel(); }
translate([5,0,6]) {channel(); }
translate([12.5,10,2.5]){cube([10,40,3.5]);}
translate([15,10,0]){cube([5,40,5]);}
}

difference(){
translate([11,55,5]){cube([13,6,20]);}
translate([12.5,57,10]){cube([10,2,15]);}
translate([15,55,13]){cube([5,6,12]);}
}
