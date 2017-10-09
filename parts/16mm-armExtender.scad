//My 16mm projector, an Ampro Imperial, could only accommodate 7 inch (400 foot) reels,
//but I had several larger ones. This arm extender, fitting between the projector and the 
//original arm, allows me to use 12" and larger reels on my projector.
//I drive the reel (only necessary when rewinding by combining two spring belts to create
//a larger one; the length of this belt dictates the length of the extender arm.
//I haven't changed the length of the takeup arm; I plan on cutting and resplicing the film,
//so that a larger reel will be stored on two separate 7" takeup reels

hole_diameter= 10;
hole_radius=hole_diameter/2;
arm_width=8;
arm_length=148; //hole to hole
outside_radius=8.5+hole_radius;

difference(){
union(){
translate([0,-outside_radius,0]) cube ([arm_length, outside_radius*2, arm_width]); //main arm
cylinder(h=arm_width, r=outside_radius);    //outside arm bottom
rotate([0,0,44]) cube([outside_radius,outside_radius, arm_width]); //arm stop
translate([arm_length,0,0])
    rotate([0,0,44]) 
    translate([-outside_radius,outside_radius,0])
    cube([outside_radius*2,outside_radius, arm_width]);
translate([arm_length,0,arm_width]) cylinder(h=arm_width, r=outside_radius);    //outside arm bottom
    
translate([arm_length-30,-outside_radius,arm_width]) cube([32, outside_radius*2, arm_width]);

}

cylinder(r=hole_radius, h=arm_width);
translate([arm_length,0,arm_width]) cylinder(r=hole_radius-.2, h=arm_width);
translate([arm_length,0,0]) cylinder(r=outside_radius-.3, h=arm_width);
translate([arm_length,0,0])
    rotate([0,0,44]) 
    cube([outside_radius*2,outside_radius, arm_width]);


}