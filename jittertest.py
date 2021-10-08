#jittertest.py
import dsocomm as dd
import dsofunctions as df
import testfunctions as tf
import baselinetest as bt
import config as cf

def jitter_test(chans) :
    tf.report_write("\n****INTERCHANNEL JITTER TEST****\n")

    df.stop_acq()

    df.set_service_access()
    dd.vbs_cmd("Acquisition.Horizontal","Maximize", "FixedSampleRate")
    dd.vbs_cmd("Acquisition.Horizontal","SampleRate", 80e9 )


    dd.vbs_cmd("Acquisition.Horizontal","HorScale", 5.0e-6)
    b = dd.wait(60)

    df.set_input_source_calsquare(chans)

    df.view_channels(1, chans)

    #dd.vbs_cmd("Acquisition.Trigger","C1Level","0.20")
    df.set_single_force_trig()

    dd.vbs_cmd("Math.F1","Source1", "C" + chans[1])
    dd.vbs_cmd("Math.F1", "Operator1", "Interpolate")
    dd.vbs_cmd("Math.F1.Operator1Setup", "Expand", 5.00)

    dd.vbs_cmd("Math.F1", "View", -1)

    dd.vbs_cmd("Math.F2","Source1", "C" + chans[0])
    dd.vbs_cmd("Math.F2", "Operator1", "Interpolate")
    dd.vbs_cmd("Math.F2.Operator1Setup", "Expand", 5.00)
    dd.vbs_cmd("Math.F2", "View", -1)


    dd.vbs_cmd("Display","GridMode","Auto")       

    dd.vbs_cmd("Measure.p2", "View", 0)

    dd.vbs_cmd("Measure", "ShowMeasure", 1)
    dd.vbs_cmd("Measure.p1", "Source1", "F2")
    dd.vbs_cmd("Measure.p1", "Source2", "F1")

    dd.vbs_cmd("Measure.P1", "View", 1)
    dd.vbs_cmd("Measure.p1", "ParamEngine", "Skew")
    dd.vbs_cmd("Measure", "StatsOn", 1)
    b = dd.std_qry("*OPC?")

    tf.measure_and_test( "jitter", "skew jitter", "sdev", 200.0e-15, 450.0e-15, chans )

    df.set_input_source_user(chans)

