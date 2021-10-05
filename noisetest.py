#noisetest.py
import dsocomm as dd
import dsofunctions as df
import config as cf
import numpy as np

def noise_test(chans) :
    seg = range(8)
    segment = np.arange(8)
    lower = 1.25*segment
    lower_limits = [-155, -155, -155, -155, -155, -155, -155, -155]
    upper_limits = [-140, -140, -140, -140, -140, -140, -140, -140]
    

    dd.vbs_cmd("Acquisition.C1", "View", 1)


    df.stop_acq()
    df.set_single_force_trig()
    df.view_channels(1, chans)  
    
    dd.vbs_cmd("Math.F1","Source1", "C" + chans[0])
    dd.vbs_cmd("Math.F1", "Operator1", "Zoom")
    dd.vbs_cmd("Math.F1", "View", -1)

       
    dd.vbs_cmd("Math.F2","Source1", "F1")
    dd.vbs_cmd("Math.F2", "Operator1", "FFT")
    dd.vbs_cmd("Math.F2.Operator1Setup", "Type", "PowerDensity")
    dd.vbs_cmd("Math.F2.Operator1Setup", "Algorithm", "LeastPrime")
    dd.vbs_cmd("Math.F2.Operator1Setup", "Window", "Rectangular")
    dd.vbs_cmd("Math.F2", "View", -1)

    dd.vbs_cmd("Display","GridMode","Auto")       

    dd.vbs_cmd("Measure", "ShowMeasure", 1)
    dd.vbs_cmd("Measure.P2", "View", 1)
    dd.vbs_cmd("Measure.p2", "ParamEngine", "area")
    dd.vbs_cmd("Measure.p2", "Source1", "F2")
    dd.vbs_cmd("Measure.P2", "GateStart", 0.00)
    dd.vbs_cmd("Measure.P2", "GateStop", 1.25)

    dd.vbs_cmd("Measure.P1", "View", 1)
    dd.vbs_cmd("Measure.p1", "MeasurementType", "math")
    dd.vbs_cmd("Measure.P1", "ArithEngine", "ParamRescale")
    dd.vbs_cmd("Measure.P1", "PSource1", "P2")
    dd.vbs_cmd("Measure.P1.Operator", "Adder", -97.00)

    # do noise spectrum integral over each of 8 segments
    for s in seg :
        dd.vbs_cmd("Measure.P2", "GateStart", lower[s])
        dd.vbs_cmd("Measure.P2", "GateStop", lower[s]+1.25)
        measurement_name = "segment {0} noise".format(s)

        df.measure_and_test( "noisespectrum", measurement_name, "out", lower_limits[s], upper_limits[s], chans )
    







