import dsocomm as dd
import dsofunctions as df
import testfunctions as tf
import baselinetest as bt
import noisetest as nt
import delaycaltests as dt
import temptest as tt
import jittertest as jt
import pyodbc as db
import config as cf
import dbfunctions as dbf
import time

# general global enables
cf.dbi_on = False
cf.database_on = False
cf.debug_on = True
cf.sim_on = False
cf.print_on = True
cf.file_on = True

# test enables
baseline_tst_on = True
noise_tst_on = False
delaycal_tst_on = False
temp_tst_on = True
jitter_tst_on = False

# channels to test
# nondbi_chans = ['1','2','3','4']
nondbi_chans = ['1' , '2','3','4','5','6','7','8']
dbi_chans = [ '2','3' ]

chans = nondbi_chans

cf.run_num = 0

tf.report_init()

num_acq_modules = 8


if cf.dbi_on :
    tf.report_write("\n**** DBI ON ****\n\n")
else :
    tf.report_write("\n**** DBI OFF ****\n\n")

str_out = "Testing channels: {0} \n".format(chans)
tf.report_write(str_out)

# Initialize 
if cf.sim_on :
    a = dd.start_dso("IP:127.0.0.1")
else :
    a = dd.start_dso("IP:10.7.10.16")

if  not a  :
    print( "Can't connect to scope.")
    quit()
if cf.debug_on :
    print(dd.std_qry("*idn?"),"\n")

# Get MCM and Acq module serial numbers
if not cf.sim_on :
    modstr = dd.std_qry("*idn?")
    mcm_sernum = df.extract_serial_nums(modstr,',')
    tf.report_write('MCM serial number = {0} \n'.format(mcm_sernum[0]))

    modstr = dd.vbs_qry("Acquisition","AcquisitionModulesStatus")
    acq_sernums = df.extract_serial_nums(modstr,' ')
    tf.report_write('Acq module serial numbers = {0} \n'.format(acq_sernums))

if cf.database_on :
    dbf.open_db("c:\Work\testdb2.mdb")
    dbf.write_runinfo_rec(num_acq_modules, mcm_sernum, acq_sernums)

df.recall_default_setup()


# Set up timebase if dbi on
if cf.dbi_on :
    df.set_dbimode(chans)

# Tests

if baseline_tst_on :
    bt.baseline_test(chans)
if noise_tst_on :
    nt.noise_test(chans)
if delaycal_tst_on :
    if not cf.dbi_on :
        dt.delaycal_test(chans)
if jitter_tst_on :
    jt.jitter_test(chans)

if temp_tst_on :
    tt.temp_test()


if cf.database_on :
    cf.conn.commit()
    cf.conn.close

tf.report_finish()


a = dd.end_dso()
