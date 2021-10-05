# temptest.py

import dsocomm as dd
import dsofunctions as df
import time
import config as cf
import matplotlib.pyplot as plt
import numpy as np


count = range(3600)
monitors = ["HSHCH1", "HSHCH2", "HSHCH3", "HSHCH4"]
tgraph = [[],[],[],[]]


def temp_test() :

    df.set_service_access()
    plt.ion()

    first = True
    for i in count :
        aout = []
        dd.vbs_cmd("MauiKernel.Acquisition.Boards(\"EagleAcqBoard\").HealthMonitor", "Refresh", "")

        for j,imon in enumerate(monitors) :
            aout.append( round(float(dd.vbs_qry("MauiKernel.Acquisition.Boards(\"EagleAcqBoard\").HealthMonitor", imon)),2) )
            tgraph[j].append(aout[j])
     
        if (i % 4) == 3 :
            if not first :
               plt.clf()

            plt.plot(tgraph[0])
            plt.plot(tgraph[1])
            plt.plot(tgraph[2])
            plt.plot(tgraph[3])
            plt.draw()
            plt.pause(0.01)

            first = False

        time.sleep(1)

    print("Save plot and then end hit enter: ")
    x = input()
 




