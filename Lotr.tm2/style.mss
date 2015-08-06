// PENCIL

// Much of the design of this style is handled by image textures.
// These were drawn by hand on paper, scanned, and tweaked in
// image editing software.

Map {
  background-image:url(img/natural_paper.png);
  background-image-opacity: 0.5;
  background-color: #F8ECC2;
  font-directory: url("fonts/");
}

#water {
  // The ::dark and ::light attachments create a subtle inner-
  // shadow on water bodies for added contrast.
  ::dark { polygon-fill: #aaa; }
  ::light14[zoom<=14],
  ::light15[zoom=15],
  ::light16[zoom=16],
  ::light17[zoom>=17] {
    polygon-fill: #F8ECC2 ;
    
    polygon-gamma: 0.5;
    image-filters: agg-stack-blur(8,8);
    image-filters-inflate: true;
  }
  ::light15[zoom=15] { image-filters: agg-stack-blur(16,16); }
  ::light16[zoom=16] { image-filters: agg-stack-blur(32,32); }
  ::light17[zoom<=17] { image-filters: agg-stack-blur(64,64); }
  // Pencil shading texture:
  ::texture {
    comp-op: multiply;
    polygon-pattern-alignment: global;
   polygon-pattern-file:url(img/water.png);
        polygon-pattern-opacity: 0.4;

  }
}

#landuse {
  opacity: 0.5;
  comp-op: multiply;
  [class='park'],
  [class='cemetery'] {
    polygon-pattern-opacity: 0.5;
    polygon-pattern-file:url(img/shade_medium.png);
    [zoom<=15] {
      line-opacity: 0.4;
      line-width: 1.2;
      [zoom=15] { line-width: 2; }
    }
    [zoom>=16] { line-pattern-file:url(img/line_shade_22.png); }
  }
}

#aeroway['mapnik::geometry_type'=2][zoom>=12] {
  comp-op: multiply;
  opacity:0.5;
  [type='taxiway'] {
    [zoom=13] { line-pattern-file:url(img/line_solid_6.png); }
    [zoom=14] { line-pattern-file:url(img/line_solid_7.png); }
    [zoom=15] { line-pattern-file:url(img/line_shade_22_1.png); }
    [zoom=16] { line-pattern-file:url(img/line_shade_22_2.png); }
    [zoom>16] { line-pattern-file:url(img/line_shade_22_4.png); }
  }
  [type='runway'] {
    line-pattern-file:url(img/line_shade_22.png);
    [zoom>=15] { line-pattern-file:url(img/line_shade_22_2.png); }
    [zoom>=16] { line-pattern-file:url(img/line_shade_22_4.png); }
  }
}

#building[zoom=15] {
  polygon-pattern-file:url(img/shade_medium.png);
  line-pattern-file:url(img/line_solid_6.png);
}
#building[zoom>=16] {
  ::shadow {
    polygon-fill: #000;
    polygon-geometry-transform:translate(0,2);
    image-filters:agg-stack-blur(3,3);
    opacity:0.3;
    
  }
  ::shadow2[zoom>=18] {
    line-pattern-file:url(img/line_shade_22.png);
    line-pattern-geometry-transform:translate(0,2);
  }
  ::fill[zoom>=15][zoom<=20] {
    polygon-pattern-file:url(img/shade_light.png);
    polygon-pattern-alignment:global;
    line-pattern-file:url(img/line_solid_6.png);
  }
}

#admin[admin_level=2] {
  ::glow[maritime=0] {
    opacity: 0.8;
    line-color: #e3e3e3;
    line-width: 6;
    line-join: round;
    [zoom>=5] { line-width: 7; }
    [zoom>=7] { line-width: 8; }
  }
  line-width:1.2;
  line-color: #666;
  line-opacity:0.8;
  line-dasharray:2,1,3,1,1,1,4,1,5,1;
  line-join: round;
  line-cap: round;
  [maritime=1] {
    line-dasharray:4,4,3,3;
    line-opacity: 0.5;
  }
  [disputed=1] {
    line-dasharray: 9,7;
  }
  [zoom>=5] { line-width: 1.8; }
  [zoom>=7] { line-width: 2.2; }
}

#admin[admin_level>=3][maritime=0] {
  ::glow[maritime=0] {
    opacity: 0.8;
    line-color: #e3e3e3;
    line-width: 4;
    line-join: round;
    [zoom>=5] { line-width: 5; }
    [zoom>=7] { line-width: 6; }
  }
  line-width: 1;
  line-color: #666;
  line-opacity:0.5;
  line-dasharray:2,1,3,1,1,1,4,1,5,1;
  line-join: round;
  line-cap: round;
  [zoom>=7] { line-width: 1.5; }
  [zoom>=10] { line-width: 2.2; }
}