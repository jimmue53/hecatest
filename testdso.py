import dsocomm as dd
import dsofunctions as df

acq_modules_to_test = [ 1,2,3,4 ]

# Create list to test all non-dbi channels in 4 modules
nondbi_chans = df.channels_to_test(acq_modules_to_test, [1])

dd.start_dso()
print(dd.std_qry("*idn?"))

df.set_service_access()

#df.set_input_source_calsquare(nondbi_chans)

df.set_input_source_user(nondbi_chans)

a = dd.end_dso()