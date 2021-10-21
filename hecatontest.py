import dsocomm as dd
import dsofunctions as df
import testfunctions as tf
import baselinetest as bt
import noisetest as nt
import delaycaltests as dt
import jittertest as jt
import pyodbc as db
import config as cf
import dbfunctions as dbf
import time

#***************** BEGIN TEST CONFIGURATION *******************

# DBI STATE FOR ALL CHANNELS UNDER TEST IS THE SAME. SET HERE:
cf.dbi_on = False

# SPECIFY CHANNELS TO TEST.  MUST BE CONSISTENT WITH dbi STATE SET ABOVE


#chans = ['1','2','3','4']
#chans = ['1','2','3','4','5','6','7','8','9','10','11','12',
#'13','14','15','16','17','18','19','20']
chans = ['1','2','3','4','5','6','7','8','9','10','11','12',
'13','14','15','16','17','18','19','20','21','22','23','24',
'25','26','27','28']
#chans = [ '2','3','6','7','10','11','14','15','18','19','22','23','26','27']

# SELECT TESTS TO RUN
baseline_tst_on  =  True
noise_tst_on     =  True
delaycal_tst_on  =  True
jitter_tst_on    =  True

# SPECIFY REPORTING OPTIONS
cf.print_on = True
cf.file_on = True
cf.database_on = False

# SPECIFY SCOPE ADDRESS
scope_address = "IP:10.7.10.16"

#******************** END TEST CONFIGURATION *******************

#******************* SPECIAL TEST CONFIGURATION ******************
# FOR USING SCOPE SIMULATOR TO WORK ON CODE
cf.sim_on = False

# USE FOR DEBUG PRINTOUTS TO WORK ON CODE
cf.debug_on = False
#******************* END OF SPECIAL TEST CONFIGURATION ************

if cf.sim_on :
    scope_address = "IP:127.0.0.1"
a = dd.start_dso(scope_address)
if  not a  :
    print( "Can't connect to scope.")
    quit()

tf.report_init()

if cf.dbi_on :
    tf.report_write("\n**** DBI ON ****\n\n")
else :
    tf.report_write("\n**** DBI OFF ****\n\n")

tf.report_write("Testing channels: {0} \n".format(chans))


# Get MCM and Acq module serial numbers
if not cf.sim_on :
    modstr = dd.std_qry("*idn?")
    mcm_sernum = df.extract_serial_nums(modstr,',')
else:
    mcm_sernum = ["sim"]

tf.report_write('MCM serial number = {0} \n'.format(mcm_sernum[0]))


if not cf.sim_on :
    modstr = dd.vbs_qry("Acquisition","AcquisitionModulesStatus")
    acq_sernums = df.extract_serial_nums(modstr,' ')
    tf.report_write('Acq module serial numbers = {0} \n'.format(acq_sernums))
else :
    acq_sernums = mcm_sernum

num_acq_modules = len(acq_sernums)

# Write new run record
if cf.database_on :
    dbf.open_db(r'c:\Work\testdb23.mdb')
    dbf.write_runinfo_rec(num_acq_modules, mcm_sernum, acq_sernums)

# Run Enabled Tests
if baseline_tst_on :
    bt.baseline_test(chans)
if noise_tst_on :
    nt.noise_test(chans)
if delaycal_tst_on :
    if not cf.dbi_on :
        dt.delaycal_test(chans)
if jitter_tst_on :
    if not cf.dbi_on :
        jt.jitter_test(chans)

# Close database
if cf.database_on :
    cf.conn.commit()
    cf.conn.close

# Close report file
tf.report_finish()

# Close scope connection
a = dd.end_dso()
