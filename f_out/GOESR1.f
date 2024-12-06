      subroutine goesr1(iwa)
      common /sixs_ffu/ s(1501),wlinf,wlsup
      real sr(1,1501),wli(1),wls(1)
      real s,wlinf,wlsup
      integer iwa,l,i
c
c    Generated from GOES-R_ABI_PFM_SRF_CWG_ch1.txt
c
      data (sr(1,l),l=1,1501)/  77*0,
     a 0.00146727, 0.01671587, 0.14467189, 0.44414738, 0.60122910, 0.74601475, 0.82896047,
     a 0.85289431, 0.92307627, 0.93636415, 0.97120691, 0.99038683, 0.99284795, 0.98600361,
     a 0.94086309, 0.91943776, 0.97206524, 0.97260960, 0.92769448, 0.58374259, 0.21363336,
     a 0.04125311, 0.00540161, 0.00112433, 0.00000000,
     a1399*0./
      wli(1)=0.4425
      wls(1)=0.504900
      do 1 i=1,1501
      s(i)=sr(iwa,i)
    1 continue
      wlinf=wli(iwa)
      wlsup=wls(iwa)
      return
      end

