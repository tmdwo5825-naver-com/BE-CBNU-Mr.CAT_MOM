from datetime import datetime


class ProcessTime():
    def get_static_time(self, day, hour, min) :
        if hour > 12:
            hour -= 12
            static_time = f"{day}일 오후 {hour}시 {min}분"
        else:
            static_time = f"{day}일 오후 {hour}시 {min}분"

        return static_time

    def get_recent_time(self, hour_ago, min_ago):
        hour_ago = int(hour_ago)
        hour_now = int(datetime.today().hour) + 9
        if hour_now < 3:
            hour_now = 24 + hour_now

        hour_recent = hour_now - hour_ago

        min_ago = int(min_ago)
        min_now = int(datetime.today().minute)
        if min_now < min_ago:
            min_now = 60 + min_now
            hour_recent -= 1

        min_recent = min_now - min_ago

        if hour_recent == 0:
            recent_time = f"{min_recent}분 전"
        else:
            recent_time = f"{hour_recent}시간 {min_recent}분 전"
        return recent_time


process_time = ProcessTime()
