import dsocomm as dd
import dsofunctions as df
import testfunctions as tf
import config as cf


def baseline_test( chans ) :
    #
    # Baseline Test
    #
    tf.report_write("\n****BASELINE TEST****\n")
    df.stop_acq()

    df.view_channels(1, chans)  
      
    tf.setup_zoom_in_F1(chans[0])
    
    # turn on P1 and set source to F1
    dd.vbs_cmd("Measure", "ShowMeasure", 1)
    dd.vbs_cmd("Measure.P1", "View", 1)
    dd.vbs_cmd("Measure.p1", "Source1", "F1")

    dd.vbs_cmd("Measure.p1", "ParamEngine", "Mean")
    tf.measure_and_test( "baseline", "Mean" , "out", -4.0e-3, 4.0e-3, chans )

    dd.vbs_cmd("Measure.p1", "ParamEngine", "Sdev")
    tf.measure_and_test( "baseline", "Sdev" , "out", 0.0, 2.0e-3, chans )


