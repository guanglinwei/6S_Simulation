      subroutine MODIS1km(iwa)
      common /sixs_ffu/ s(1501),wlinf,wlsup
      real sr(12,1501),wli(12),wls(12)
      real wlinf,wlsup,s
      integer iwa,l,i

c band 8 of MODIS1km - 416 (cw=416nm)
      data (sr(1,l),l=1,1501,1) / 61*0.,
     A .0832, .4966, .6172, .7460, .4824, .8323, .8906, .3203,
     A .0308,
     A1431*0./

c band 9 of MODIS1km - 442 (cw=442nm)
      data (sr(2,l),l=1,1501,1) / 73*0.,
     A .0050, .0989, .5052, .9311, .9998, .9425, .3859, .0367,
     A 
     A1420*0./

c band 10 of MODIS1km - 489 (cw=489nm)
      data (sr(3,l),l=1,1501,1) / 91*0.,
     A .0050, .1000, .5752, .9432, .9877, .9881, .5907, .0342,
     A 
     A1402*0./

c band 11 of MODIS1km - 530 (cw=530nm)
      data (sr(4,l),l=1,1501,1) / 108*0.,
     A .0112, .1848, .6871, .9800, .9984, .9300, .7037, .2516,
     A .0202,
     A1384*0./

c band 12 of MODIS1km - 547 (cw=547nm)
      data (sr(5,l),l=1,1501,1) / 115*0.,
     A .0121, .1571, .5719, .9671, .9919, .8729, .5080, .0772,
     A 
     A1378*0./

c band 13 of MODIS1km - 665 (cw=665nm)
      data (sr(6,l),l=1,1501,1) / 163*0.,
     A .0470, .3321, .7801,1.0000, .8878, .6768, .2774, .0162,
     A 
     A1330*0./

c band 14 of MODIS1km - 677 (cw=677nm)
      data (sr(7,l),l=1,1501,1) / 167*0.,
     A .0344, .1874, .5695, .9352, .9904, .9292, .6282, .2088,
     A .0230,
     A1325*0./

c band 15 of MODIS1km - 747 (cw=747nm)
      data (sr(8,l),l=1,1501,1) / 195*0.,
     A .0295, .1989, .5810, .9240, .9906, .7709, .3820, .0574,
     A .0060,
     A1297*0./

c band 16 of MODIS1km - 865 (cw=865nm)
      data (sr(9,l),l=1,1501,1) / 241*0.,
     A .0179, .0834, .2825, .5989, .8807, .9995, .9796, .9444,
     A .7581, .4820, .1475, .0270, .0056,
     A1247*0./

c band 17 of MODIS1km - 902 (cw=902nm)
      data (sr(10,l),l=1,1501,1) / 249*0.,
     A .0149, .0258, .0490, .0962, .1865, .3339, .5393, .7619,
     A .8979, .9532, .9854, .9952,1.0000, .9984, .9814, .9632,
     A .9584, .9506, .8812, .7020, .4410, .2356, .1210, .0644,
     A .0367, .0210, .0122,
     A1225*0./

c band 18 of MODIS1km - 936 (cw=936nm)
      data (sr(11,l),l=1,1501,1) / 269*0.,
     A .0050, .0588, .2425, .5456, .8591, .9870, .9882, .9023,
     A .6191, .2772, .0566,
     A1221*0./

c band 19 of MODIS1km - 941 (cw=941nm)
      data (sr(12,l),l=1,1501,1) / 256*0.,
     A .0132, .0203, .0307, .0456, .0657, .0951, .1430, .2264,
     A .3499, .5088, .6569, .7597, .8162, .8507, .8851, .9216,
     A .9414, .9445, .9521, .9744, .9988, .9951, .9969, .9895,
     A .9588, .8874, .7637, .6031, .4450, .3126, .2107, .1390,
     A .0887, .0581, .0391, .0275, .0206, .0167, .0137, .0114,
     A 
     A1205*0./

c lower and upper wavelength
      wli(1)=0.4025
      wls(1)=0.4225
      wli(2)=0.4325
      wls(2)=0.4500
      wli(3)=0.4775
      wls(3)=0.4950
      wli(4)=0.5200
      wls(4)=0.5400
      wli(5)=0.5375
      wls(5)=0.5550
      wli(6)=0.6575
      wls(6)=0.6750
      wli(7)=0.6675
      wls(7)=0.6875
      wli(8)=0.7375
      wls(8)=0.7575
      wli(9)=0.8525
      wls(9)=0.8825
      wli(10)=0.8725
      wls(10)=0.9375
      wli(11)=0.9225
      wls(11)=0.9475
      wli(12)=0.8900
      wls(12)=0.9875


      do 1 i=1,1501
      s(i)=sr(iwa,i)
    1 continue
      wlinf=wli(iwa)
      wlsup=wls(iwa)
      return
      end