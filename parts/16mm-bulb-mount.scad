//A mount designed to connect an MR16 led lamp to the end of the lens of my 16mm projector. 
//You will need to modify the diameters to fit your own parts.

lens_diameter=36.6;
bulb_diameter=49.5;
height=10;
coneheight=20;
insidetop=lens_diameter/2+.5;
outsidetop=lens_diameter/2+4;  
insidebottom=bulb_diameter/2+.5;
outsidebottom=bulb_diameter/2+4;
difference(){
    union(){
        translate([0,0,height+coneheight]){
            difference(){
                cylinder (h=height, r=outsidetop );
                cylinder (h=height, r=insidetop);}
            }
        translate([0,0,height]){
            difference(){
                cylinder(h=coneheight, r1=outsidebottom, r2=outsidetop);
                cylinder(h=coneheight, r1=insidebottom, r2=insidetop);}
            }
        difference(){
            cylinder (h=height, r=outsidebottom);
            cylinder (h=height, r=insidebottom);}
         }
    //Subtract cutouts from cylinders surrounding lens and bulb, to allow more 'give' when connecting mount and lamp/lens
    translate([-5,-50,0]) cube([10,100,height+1/3*coneheight]);
    translate([-50,-5,0]) cube([100,10,coneheight]);
    translate([-5,-50,height+coneheight]) cube([10,100,coneheight]);
    translate([-50,-5,height+coneheight]) cube([100,10,coneheight]);


}