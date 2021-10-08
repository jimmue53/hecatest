import dsocomm as dd
import dsofunctions as df
import testfunctions as tf
import baselinetest as bt
import config as cf

def delaycal_test(chans) :
    tf.report_write("\n****DELAYCAL SIGNAL TEST****\n")
    
    df.stop_acq()

    df.set_service_access()
 
    dd.vbs_cmd("Acquisition.Horizontal","HorScale",1.0E-9)
    b = dd.wait(60)

    df.set_input_source_calsquare(chans)

    df.view_channels(1, chans)

    #dd.vbs_cmd("Acquisition.Trigger","C1Level","0.20")
    df.set_single_force_trig()

    tf.setup_zoom_in_F1(chans[0])
    
    # turn on P1 and set source to F1
    dd.vbs_cmd("Measure", "ShowMeasure", 1)
    dd.vbs_cmd("Measure.P1", "View", 1)
    dd.vbs_cmd("Measure.p1", "Source1", "F1")

    dd.vbs_cmd("Measure.p1", "ParamEngine", "TimeAtLevel")
    tf.measure_and_test( "delaycal", "TimeAtLevel" , "out", -3.0e-9,3.0e-9, chans )

    dd.vbs_cmd("Measure.p1", "ParamEngine", "Rise2080")
    tf.measure_and_test( "delaycal", "Rise2080" , "out", 15.0e-12,25.0e-12, chans )

    dd.vbs_cmd("Measure.p1", "ParamEngine", "Amplitude")
    tf.measure_and_test( "delaycal", "Amplitude" , "out", 0.20, 0.5, chans )

   



    df.set_input_source_user(chans)
 




