import dsocomm as dd
import config as cf
import pyodbc as db
import dbfunctions as dbf
import dsofunctions as df
import time


def setup_zoom_in_F1(source) :
    # source is the ascii channel identifier of the source waveform, e.g., "C1"
    dd.vbs_cmd("Math.F1","Source1", source)
    dd.vbs_cmd("Math.F1", "Operator1", "Zoom")
    dd.vbs_cmd("Math.F1", "View", -1)



def measure_and_test( testname, measurement_name, measure_type, lower_limit, upper_limit, chans_to_test ) :
    # This function assumes the measurement is already set up by the calling routine.
    # It assumes that the channel under test is used as source for F1.
    # So it will change the source for F1 to loop through channels.
    # This function assumes the output measurement will be on P1.

    for chan in chans_to_test :
        dd.vbs_cmd("Math.F1","Source1", "C" + chan)

        df.set_single_force_trig()
        dd.wait(10)
        b = dd.std_qry("*OPC?")
        
        # Get regular output or sdev depending on measurement type
        measure_val = float(dd.vbs_qry("measure.p1." + measure_type + ".result", "value"))
        
        # compare measurement against test limits
        test_result = "Yes"
        if (measure_val < lower_limit) or (measure_val > upper_limit)  :
            test_result = "No"

        # conditions for measurement - dbi state and channel #
        if cf.dbi_on :
            cond1 = "dbi_on"
        else:
            cond1 = "dbi_off"
        cond2 = "C" + chan

        # print result            
        report_write('C{:2s}  {:15s}  {:>14.3e}  {:4s}  \n'.format(chan,measurement_name,measure_val, test_result) )
        
        # Write results to database if enabled
        if cf.database_on :
            fields = "run_index, test_name, cond1, cond2, measure_name, measure_value, pass"
            values = "{0}, '{1}', '{2}', '{3}', '{4}', {5}, {6}".format(
                cf.run_num, testname, cond1, cond2, measurement_name, measure_val, test_result)
            str="INSERT INTO testresult( {0} ) VALUES( {1} )".format(fields, values)
            cf.cursor.execute(str )

def report_init() :
    asc_time = time.asctime()
    start_time = asc_time.replace(' ', '_')
    start_time = start_time.replace(':', '')
    str_out = "\n\n\n***********   Begin Hecatest - {0}  ***********\n".format(asc_time)
    if cf.print_on :
        print(str_out)
    if cf.file_on :
        cf.fh = open("c:\Work\Hecadata\Hecatest_{0}".format(start_time),'w' )
        cf.fh.write(str_out)

def report_write(str_out) :
    if cf.print_on :
        print(str_out)
    if cf.file_on :
        cf.fh.write(str_out)

def report_finish() :
    if cf.file_on :
        cf.fh.close()
