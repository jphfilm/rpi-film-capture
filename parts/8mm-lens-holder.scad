//I purchased a few loose triplet lenses from surplusshed.com
//This is a holder for one of them, designed to fit into the camera mount specified in another file
//Printed in black ABS so as to absorb light and be slightly softer,
// since it has to fit into the camera mount. 
lens_diameter= 15;
lens_cushion=  .5;
lens_radius = (lens_diameter+lens_cushion)/2;
lens_height = 11;
mount_diameter = 20;
mount_cushion = .5;
mount_radius = (mount_diameter-mount_cushion)/2;

difference() {
cylinder (h=lens_height, r=mount_radius);
cylinder (h=lens_height, r=lens_radius);
translate([0,0,9]) {cylinder(h=2, r1=lens_radius, r2=mount_radius);}
}