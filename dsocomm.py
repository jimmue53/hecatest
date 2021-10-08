import win32com.client
import config as cf
# from time import sleep
from math import *

def start_dso(connection_string):
    global _dso
    _dso=win32com.client.Dispatch("LeCroy.ActiveDSOCtrl.1")
    r = _dso.MakeConnection(connection_string)
    return r

def end_dso():
    global _dso
    r = _dso.Disconnect()
    return r

def vbs_cmd( path , control = "" , value="" ):
    global _dso
    outstring = "VBS 'app"
    if path != "" :
        outstring = outstring + "." + path
    outstring = outstring + "." + control

    if value != "" :
        if isinstance(value, str):
            valstr = "=\"{0}\"".format(value)
        else:
            valstr = "={0}".format(value)
    else:
        valstr = ""   
    outstring = outstring + valstr + "'"
    _dso.WriteString(outstring , True)

# arguments for method are passed in a list
def vbs_method( path , control = "" , value=[] ):
    global _dso
            
    outstring = "VBS? " + "'Return = app."+path + "." + control 
    outstring = outstring + "( "
    for arg in value :
        if value.index(arg) != 0 :
            outstring = outstring + ", "
        outstring = outstring + "{0}".format(arg)
    outstring = outstring +" )'"
    _dso.WriteString(outstring , True)
    r = _dso.ReadString(200)
    if r == 0 :
        print("Qry error, outstring = " + outstring + "r = ", r)
    return r

def vbs_qry(path , control):
    global _dso
    outstring = "VBS? " + "'Return = app."+path + "." + control + "'"
    _dso.WriteString(outstring , True)
    r = _dso.ReadString(400)
    if r == 0 :
        print("Qry error, outstring = " + outstring + "r = ", r)
    return r

def wait(timeout):
    global _dso
    outstring = "VBS? " + "'Return = app.WaitUntilIdle(" + "{0}".format(timeout) + ")'"
    #print("wait outstring = " +  outstring)
    _dso.WriteString(outstring , True)
    r = _dso.ReadString(200)
    if r == 0 :
        print( "WaitUntilIdle expired, return = ", r)
    return r

def operation_complete():
    global _dso
    _dso.WriteString("*OPC?" , True)
    return _dso.ReadString(200)


def std_qry(instring):
    global _dso
    _dso.WriteString(instring , True)
    return _dso.ReadString(200)

def std_cmd(instring):
    global _dso
    _dso.WriteString(instring, True)




