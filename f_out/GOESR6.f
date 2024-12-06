      subroutine goesr6(iwa)
      common /sixs_ffu/ s(1501),wlinf,wlsup
      real sr(1,1501),wli(1),wls(1)
      real s,wlinf,wlsup
      integer iwa,l,i
c
c    Generated from GOES-R_ABI_PFM_SRF_CWG_ch6.txt
c
      data (sr(1,l),l=1,1501)/  778*0,
     a 0.00108148, 0.00196354, 0.00348948, 0.00550978, 0.01039215, 0.01801874, 0.03656100,
     a 0.07428630, 0.15076788, 0.29894792, 0.52472886, 0.76543663, 0.91827611, 0.96180273,
     a 0.96199855, 0.96110387, 0.97088104, 0.98646455, 0.99881086, 0.99929715, 0.99581052,
     a 0.99035918, 0.98177882, 0.96345876, 0.95016787, 0.94009006, 0.90969956, 0.80263712,
     a 0.59813220, 0.35470806, 0.17368217, 0.07878266, 0.03640565, 0.01770432, 0.00944380,
     a 0.00492774, 0.00298107, 0.00192096, 0.00000000,
     a684*0./
      wli(1)=2.1950
      wls(1)=2.292400
      do 1 i=1,1501
      s(i)=sr(iwa,i)
    1 continue
      wlinf=wli(iwa)
      wlsup=wls(iwa)
      return
      end
