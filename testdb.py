import pyodbc as db

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
