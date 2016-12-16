//See 8mm-carriage.scad for documentation

TOTAL_WIDTH=30;
BORDER_WIDTH=3;
BORDER_HEIGHT=45;

//Base
difference() {
translate([-8,-3,0]){
cube([20,36,1]);
}
translate([-4,5,0]) {cube([3,20,3]);}
}

difference(){
//Main Structure
 translate([-BORDER_WIDTH,0,0]){
  cube([BORDER_WIDTH,TOTAL_WIDTH,BORDER_HEIGHT]);
 }

//Camera Opening
translate([-BORDER_WIDTH-1,10,8]){
   cube([9,9,9]);
  }
 
 translate([-BORDER_WIDTH-1,10,8]){
   cube([3,9,19]);
  }
  
//Camera Seating area  
  translate([-BORDER_WIDTH-1,2,2]){
   cube([BORDER_WIDTH/2,25,25]);
  }
}

//4 Posts
translate([-5,4,11]){
  rotate([0,90,0]){
   cylinder(h=3,r=0.75,center=true);
  }
 }

translate([-5,25,11]){
  rotate([0,90,0]){
   cylinder(h=3,r=0.75,center=true);
  }
 }
 
translate([-5,4,23.5]){
  rotate([0,90,0]){
   cylinder(h=3,r=0.75,center=true);
  }
 }

translate([-5,25,23.5]){
  rotate([0,90,0]){
   cylinder(h=3,r=0.75,center=true);
  }
 }

translate([2.5,14.5,12.5]){
  difference(){
  rotate([0,90,0]){
   cylinder(h=5,r=12, center=true);
  }
    rotate([0,90,0]){
   cylinder(h=6,r=9.75, center=true);
  }
 }
 }
 