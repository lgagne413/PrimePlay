import apps
import time
t0=time.process_time()
app = apps.findprime3()
app.run()
time.process_time()
del app