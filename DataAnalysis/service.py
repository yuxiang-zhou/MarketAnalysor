import subprocess
import time
import datetime

if __name__ == '__main__':
    hour_last = 0
    day_last = -1
    print 'Fetching Service Started'
    while True:
        dt = datetime.datetime.now()
        hour_now = dt.hour

        print 'Schedualling check'

        if dt.day != day_last and hour_now > 10:
            day_last = dt.day
            subprocess.call(["python", "fetch.py" , "-a"])
            subprocess.call(["python", "fetch.py" , "-il"])
            subprocess.call(["python", "fetch.py" , "-s"])
            subprocess.call(["python", "analysis.py" , "-p"])

        if hour_now != hour_last and hour_now % 2 ==0:
            hour_last = hour_now
            subprocess.call(["python", "fetch.py" , "-tn"])

        print 'Done, next check in 10 mins'
        time.sleep(600)
