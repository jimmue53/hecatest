import dsocomm as dd
import dsofunctions as df
import config as cf


def baseline_test( chans ) :
    #
    # Baseline Test
    #
    
    df.stop_acq()

    df.view_channels(1, chans)  
      

    df.setup_measure_and_test('baseline',[["Mean",-4.0e-3,4.0e-3] , ["Sdev",0.0,2.0e-3]], chans)


