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
        command = "Dbi" + chan + "Mode"
        dd.vbs_cmd("Acquisition.Horizontal", command, cmd_val)
        a = dd.operation_complete()

def view_channels(on , chans) :
    for ichan in chans :
        dd.vbs_cmd("Acquisition.C"+ichan, "View", on)
        b=dd.wait(60) 
    dd.vbs_cmd("Display","GridMode","Auto")       

def extract_serial_nums(instr,splitchar) :
    instrsplt=instr.split(splitchar)
    splto = []
    for s in instrsplt :
        if "LCRY" in s :
            s = s.strip('"')
            splto.append(s)
    return splto



