import dsocomm as dd
import dsofunctions as df
import baselinetest as bt
import noisetest as nt
import delaycaltests as dt
import temptest as tt
import jittertest as jt
import pyodbc as db
import config as cf
import dbfunctions as dbf

cf.run_num = 0

num_acq_modules = 1
acq_modules_to_test = [ 1 ]

# Create list to test all non-dbi channels in 4 modules
nondbi_chans = df.channels_to_test(acq_modules_to_test, [1, 2, 3, 4])

# Create list to test all DBI channels (2 and 3 ) in 4 modules
dbi_chans = df.channels_to_test(acq_modules_to_test, [2,3])

# Create list to test 1st non-dbi channel in 4 modules
first_chans = df.channels_to_test(acq_modules_to_test, [1])

chans = nondbi_chans
print("Channels to test: \n", chans)

# general global enables
cf.dbi_on = False
cf.database_on = False
cf.debug_on = True
cf.sim_on = False

# test enables
baseline_tst_on = True
noise_tst_on = False
delaycal_tst_on = False
temp_tst_on = False
jitter_tst_on = True


# Initialize 
if cf.sim_on :
    a = dd.start_dso("IP:127.0.0.1")
else :
    a = dd.start_dso("IP:10.7.10.36")

if  not a  :
    print( "Can't connect to scope.")
    quit()
if cf.debug_on :
    print(dd.std_qry("*idn?"),"\n")

# Get MCM and Acq module serial numbers
if not cf.sim_on :
    modstr = dd.std_qry("*idn?")
    mcm_sernum = df.extract_serial_nums(modstr,',')
    print('MCM serial number = {0} \n'.format(mcm_sernum[0]))

    modstr = dd.vbs_qry("Acquisition","AcquisitionModulesStatus")
    acq_sernums = df.extract_serial_nums(modstr,' ')
    print('Acq module serial numbers = {0} \n'.format(acq_sernums))

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


a = dd.end_dso()
