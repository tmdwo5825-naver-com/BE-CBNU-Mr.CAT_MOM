from math import radians, sin, cos, sqrt, atan2


async def check_location(lat, lon) -> str:
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # 지구의 반경(단위: km)

        # 위도, 경도를 라디안으로 변환
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Haversine 공식
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c

        return distance

    # 각 지점의 좌표와 범위 설정
    yangsungjae = ((36.62656935117971 + 36.62981656325492) / 2, (127.4515271608071 + 127.45543688761717) / 2, 0.2)
    n14 = ((36.63013839671825 + 36.631698348276466) / 2, (127.45610960893917 + 127.458198409401) / 2, 0.1)
    jungdo_solt = ((36.62842402748002 + 36.62989716070364) / 2, (127.45551254530146 + 127.45791941588986) / 2, 0.3)
    yangjjae = ((36.623792267078755 + 36.62624935703808) / 2, (127.45667591155414 + 127.45979841801855) / 2, 0.15)

    # 입력된 좌표와 각 지점의 거리를 계산하여 해당 범위 내인 경우 해당 지점 이름을 반환
    if haversine(lat, lon, *yangsungjae[:2]) <= yangsungjae[2]:
        return "sungjae"
    elif haversine(lat, lon, *n14[:2]) <= n14[2]:
        return "n14"
    elif haversine(lat, lon, *jungdo_solt[:2]) <= jungdo_solt[2]:
        return "lib"
    elif haversine(lat, lon, *yangjjae[:2]) <= yangjjae[2]:
        return "jinjae"
    else:
        return "else"





# 양성재 좌측하단 36.62656935117971, 127.4515271608071  /우측상단 36.62981656325492, 127.45543688761717

# 개성재 좌측하단 36.63013839671825, 127.45610960893917  /우측상단 36.631698348276466, 127.458198409401

# 솔못 좌측하단 36.62842402748002, 127.45551254530146  /우측상단 36.62989716070364, 127.45791941588986

# 양진재  좌측하단 36.623792267078755, 127.45667591155414  /우측상단 36.62624935703808, 127.45979841801855

