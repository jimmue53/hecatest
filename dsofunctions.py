import dsocomm as dd
import config as cf
import pyodbc as db
import dbfunctions as dbf


def stop_acq() :
    dd.vbs_cmd("Acquisition","Triggermode","Stopped")

def recall_default_setup() :
    dd.vbs_cmd("", "SetToDefaultSetup", "")
    b = dd.wait(120)

def set_single_force_trig() :
    dd.vbs_cmd("Acquisition","TriggerMode","Single")
    a = dd.vbs_method("Acquisition", "Acquire", [0.1 , 1])
    a = dd.wait(120)

def set_service_access() :
    dd.vbs_cmd("Utility.Service","ServiceAccessCode",14691)
    b = dd.wait(5)

def set_input_source_calsquare(chans=[]) :
    set_service_access()
    for ichan in chans :
        d = "MauiKernel.Acquisition.Boards(\"EagleAcqBoard\").Channels(\"" + "C" + ichan + "\")"
        dd.vbs_cmd(d , "InputSource", "CalSquare")
        b=dd.wait(60)

def set_input_source_user(chans=[]) :
    set_service_access()
    for ichan in chans :
        d = "MauiKernel.Acquisition.Boards(\"EagleAcqBoard\").Channels(\"" + "C" + ichan + "\")"
        dd.vbs_cmd(d , "InputSource", "User")
        b=dd.wait(60)

def channels_to_test(acq_modules_to_test, mod_chans) :
    # acq_modules_to_test = list of modules to test, integers, 1 is first
    # mod_chans = list of channels to test in every module in module list, integers
    # chans = list to be returned which contains ascii names of channels to test
    chans = []
    for which_module in acq_modules_to_test :
        start = (which_module - 1)*4
        for which_chan in mod_chans :
            indstr = "{0}".format(which_chan + start)
            chans.append( indstr )
    return chans

def set_dbimode( chans) :
    if cf.dbi_on :
        cmd_val = "DBION"
    else :
        cmd_val = "DBIOFF"
    for chan in chans :
        command = "DbiC" + chan + "Mode"
        dd.vbs_cmd("Acquisition.Horizontal", command, cmd_val)
        a = dd.operation_complete()

def view_channels(on , chans) :
    for ichan in chans :
        dd.vbs_cmd("Acquisition.C"+ichan, "View", on)
        b=dd.wait(60) 
    dd.vbs_cmd("Display","GridMode","Auto")       

def setup_measure_and_test( testname, measurements_to_do, chans_to_test ) :
    # use this functionf for simple single parameter measurements
    # It will setup the measurement parameter as well as measure and test against limits
    # If measurement setup is more complicated, use measure_and_test function.
    #
    dd.vbs_cmd("Measure", "ShowMeasure", 1)
    dd.vbs_cmd("Measure.P1", "View", 1)
    for measure_test in measurements_to_do :
        measure = measure_test[0]
        lower_limit = measure_test[1]
        upper_limit = measure_test[2]
        dd.vbs_cmd("Measure.p1", "ParamEngine", measure)
        for chan in chans_to_test :
            dd.vbs_cmd("Measure.p1", "Source1", "C" + chan)

            set_single_force_trig()
            dd.wait(10)
            b = dd.std_qry("*OPC?")
            measure_val = float(dd.vbs_qry("measure.p1.out.result", "value"))
            test_result = "Yes"
            if (measure_val < lower_limit) or (measure_val > upper_limit)  :
                test_result = "No"
                     
            print('C{:2s}  {:15s}  {:>14.3e}  {:4s}  '.format(chan,measure,measure_val, test_result) )
            if cf.database_on :
                if cf.dbi_on :
                    cond1 = "dbi_on"
                else:
                    cond1 = "dbi_off"
                cond2 = "C" + chan
                fields = "run_index, test_name, cond1, cond2, measure_name, measure_value, pass"
                values = "{0}, '{1}', '{2}', '{3}', '{4}', {5}, {6}".format(
                    cf.run_num, testname, cond1, cond2, measure, measure_val, test_result)
                str="INSERT INTO testresult( {0} ) VALUES( {1} )".format(fields, values)
                # print(str)
                cf.cursor.execute(str )

def measure_and_test( testname, measurement_name, measure_type, lower_limit, upper_limit, chans_to_test ) :
    # This function assumes the measurement is already set up by the calling routine.
    # It assumes that the channel under test is used as source for F1.
    # So it will change the source for F1 to loop through channels.
    # This function assumes the output measurement will be on P1.

    for chan in chans_to_test :
        dd.vbs_cmd("Math.F1","Source1", "C" + chan)

        set_single_force_trig()
        dd.wait(10)
        b = dd.std_qry("*OPC?")
        if measure_type == "out" :
            measure_val = float(dd.vbs_qry("measure.p1.out.result", "value"))
        if measure_type == "sdev" :
            measure_val = float(dd.vbs_qry("measure.p1.sdev.result", "value"))
        test_result = "Yes"
        if (measure_val < lower_limit) or (measure_val > upper_limit)  :
            test_result = "No"
                    
        print('C{:2s}  {:15s}  {:>14.3e}  {:4s}  '.format(chan,measurement_name,measure_val, test_result) )
        if cf.database_on :
            if cf.dbi_on :
                cond1 = "dbi_on"
            else:
                cond1 = "dbi_off"
            cond2 = "C" + chan
            fields = "run_index, test_name, cond1, cond2, measure_name, measure_value, pass"
            values = "{0}, '{1}', '{2}', '{3}', '{4}', {5}, {6}".format(
                cf.run_num, testname, cond1, cond2, measurement_name, measure_val, test_result)
            str="INSERT INTO testresult( {0} ) VALUES( {1} )".format(fields, values)
            # print(str)
            cf.cursor.execute(str )



def extract_serial_nums(instr,splitchar) :
    instrsplt=instr.split(splitchar)
    splto = []
    for s in instrsplt :
        if "LCRY" in s :
            s = s.strip('"')
            splto.append(s)
    return splto



