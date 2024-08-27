import pandas as pd
from datetime import *

def getTotalVoiceTime():
    file = pd.read_csv("data/voice_logging.csv",encoding='ISO-8859-1')

    total_time = timedelta()

    for time_str in file["total_duration"]:
        time_str = str(time_str)
        if time_str.count(":") > 0:
            total_time += parse_time(time_str)

    print(total_time)

def parse_time(time_str):
    h, m, s = time_str.split(':')
    s, ms = divmod(float(s),1)
    return timedelta(hours=int(h), minutes=int(m), seconds=int(s), milliseconds=int(ms * 1000))



getTotalVoiceTime()