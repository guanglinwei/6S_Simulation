c c                       print of final results                         c
c c                                                                      c
c c                 The following code has been edited                   c
c c               manually to only output necessary data.                c
c c       If you would like additional outputs from the simulation,      c
c c              please look in the original 6S main.f file              c
c c            and make edits, and paste the final block here.           c
c c**********************************************************************c
c       direct irradiance ratio and atmospheric path reflectance
        if(inhomo.ne.0) then
          write(iwr, 432)(aini(1,j),j=1,3), (ainr(1,j),j=1,3)

          endif
          if(inhomo.eq.0) then
          write(iwr, 432)(aini(1,j),j=1,3), (ainr(1,j),j=1,3)
          endif

c c**********************************************************************c
c c                                                                      c
c c                    print of complementary results                    c
c c                                                                      c
c c**********************************************************************c
c       global gas transmittance total
      write(iwr, 931)tgasm
c       downward and upwards scattering transmittance total
      write(iwr, 931)sdtott
      write(iwr, 931)sutott
c       spherical albedo
      write(iwr, 931)sast
c       optical depth total
      write(iwr, 931)sodtot
  432 format (3(f0.3, 1x), 3(f0.3, 1x))
  931 format(f0.5, 1x)
 1500 format(1h*,1x,42hwave   total  total  total  total  atm.   ,
     s           33hswl    step   sbor   dsol   toar ,t79,1h*,/,
     s  1h*,1x,42h       gas    scat   scat   spheri intr   ,t79,1h*,/,
     s  1h*,1x,42h       trans  down   up     albedo refl   ,t79,1h*)
 1501 format(1h*,6(F6.4,1X),F6.1,1X,4(F6.4,1X),t79,1h*)

        end
