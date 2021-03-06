import pyodbc as db
import config as cf

def open_db(filepath):
    if cf.database_on :
        connectstr = r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + filepath + ';'
        cf.conn = db.connect(connectstr)
        cf.cursor = cf.conn.cursor()

def write_runinfo_rec(num_acq_modules, mcm_sernum, acq_sernums):
    if cf.database_on :
        fields= "num_acq_units, mcm_SN"
        values="{0}, '{1}'".format(num_acq_modules, mcm_sernum[0])
        for i,sn in enumerate(acq_sernums) :
            str = ", acq_module_SN_{0}".format(i+1)
            fields = fields + str
            str = ", '{0}'".format(sn)
            values = values + str
        str="INSERT INTO runinfo( {0} ) VALUES( {1} )".format(fields, values)
        if cf.debug_on :
            print(str)
        # get run number to be entered with testresult records
        cf.cursor.execute(str )
        cf.cursor.execute('SELECT * FROM runinfo WHERE run_index=(SELECT MAX(run_index) FROM runinfo)')
        cf.run_num = cf.cursor.fetchone()[0]
        print("run_num = {0} \n".format(cf.run_num))

def testpyodbc() :
    # Obsolete - was used to initially try pyodbc functionality
    #
    conn = db.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=c:\Work\testdb2.mdb;')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO runinfo(num_acq_units) VALUES (4)")
    cursor.execute('SELECT * FROM runinfo WHERE run_index=(SELECT MAX(run_index) FROM runinfo)')
    run_num = cursor.fetchone()[0]
    print("run_num =",run_num)


    meas = ".0045"
    cursor.execute("INSERT INTO TESTRESULT(run_index, test_name,measure_name,use_value,measure_value,pass) VALUES (1,'baseline','max',True,"+meas+",True)")

    conn.commit()
    conn.close
 