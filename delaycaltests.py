import dsocomm as dd
import dsofunctions as df
import baselinetest as bt
import config as cf

def delaycal_test(chans) :
    df.stop_acq()

    df.set_service_access()
 
    dd.vbs_cmd("Acquisition.Horizontal","HorScale",1.0E-9)
    b = dd.wait(60)

    df.set_input_source_calsquare(chans)

    df.view_channels(1, chans)

    #dd.vbs_cmd("Acquisition.Trigger","C1Level","0.20")
    df.set_single_force_trig()

    df.setup_measure_and_test("delaycal", [["TimeAtLevel",-3.0e-9,3.0e-9] , ["Rise2080",15.0e-12,25.0e-12] , ["Amplitude", 0.20, 0.5]], chans)

    df.set_input_source_user(chans)
 




