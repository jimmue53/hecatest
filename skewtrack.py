# temptest.py

import dsocomm as dd
import dsofunctions as df
import testfunctions as tf
import time
import config as cf
import matplotlib.pyplot as plt
import numpy as np


count = range(30)
tgraph = []


#a = dd.start_dso("IP:127.0.0.1")
a = dd.start_dso("IP:10.7.10.16")
if  not a  :
    print( "Can't connect to scope.")
    quit()

df.set_service_access()
plt.ion()

dd.vbs_cmd("Measure", "ShowMeasure", 1)
dd.vbs_cmd("Measure.P1", "View", 1)
dd.vbs_cmd("Measure.p1", "Source1", "C1")

dd.vbs_cmd("Measure.p1", "ParamEngine", "TimeAtLevel")



first = True
for i in count :
    dd.vbs_cmd("","clearsweeps")
    df.set_single_force_trig()

    
    val = float(dd.vbs_qry("Measure.P1.out.Result" , "Value"))

    tgraph.append(val)
    
    plt.clf()

    plt.plot(tgraph)
    plt.draw()
    plt.pause(0.01)

    first = False

    time.sleep(1)

print("Save plot and then end hit enter: ")
x = input()





