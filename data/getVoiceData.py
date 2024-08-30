import pandas as pd
from datetime import *

def getTotalVoiceTime():
    file = pd.read_csv("data/voice_logging.csv", encoding='ISO-8859-1')

    total_time = timedelta()

    for time_str in file["total_duration"]:
        time_str = str(time_str)
        if time_str.count(":") > 0:
            total_time += parse_time(time_str)

    print(total_time)

def parse_time(time_str):
    # '1 day, 2:03:04'와 같은 형식을 파싱합니다.
    if 'day' in time_str:
        days, time_part = time_str.split(' day, ')
        days = int(days)
    else:
        days = 0
        time_part = time_str

    h, m, s = time_part.split(':')
    s, ms = divmod(float(s), 1)
    return timedelta(days=days, hours=int(h), minutes=int(m), seconds=int(s), milliseconds=int(ms * 1000))

getTotalVoiceTime()
