import imghdr
import imageio.v2 as imageio
from tempfile import NamedTemporaryFile
from typing import IO
from math import radians, sin, cos, sqrt, atan2


from .. database.set_mysql import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 파일을 임시적으로 서버에 저장한다.
async def save_file(file: IO):
    with NamedTemporaryFile("wb", delete=False) as tempfile:
        tempfile.write(file.read())
        return tempfile.name


# 이미지 처리 함수 heic, jpg형식에 따라 파일 처리를 달리 한다.
def process_image(file_path):
    image_format = imghdr.what(file_path)  # Check the image format

    if image_format == "heic":
        # Convert HEIC image to JPEG
        jpeg_path = "converted.jpg"
        image = imageio.imread(file_path)
        imageio.imsave(jpeg_path, image)
        return jpeg_path
    elif image_format == "jpeg" or image_format == "png":
        return [file_path, image_format]
    else:
        raise ValueError("Unsupported image format")


def check_location(x, y) -> str:
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

    # 각 지점의 좌표
    yangsungjae = (36.62785410610158, 127.45313788589664)
    n14 = (36.63054690049551, 127.4568566387854)
    jungdo_solt = (36.628825506703954, 127.45738760306085)

    # 입력된 좌표와 각 지점의 거리를 계산하여 200m 반경 이내인 경우 해당 지점 이름을 반환
    if haversine(x, y, *yangsungjae) <= 0.2:
        return "yang"
    elif haversine(x, y, *n14) <= 0.2:
        return "n14"
    elif haversine(x, y, *jungdo_solt) <= 0.2:
        return "lib"
    else:
        return "else"

##########
# 양성재 : 위도 : 36.62785410610158, 경도 : 127.45313788589664
# to 경도 127.45369324608023 or 60m
# n14쪽 : 좌표 : 위도 : 36.63054690049551, 경도 : 127.4568566387854
# to  경도 : 127.45804532282344 or 60m
# 중도 or 솔못 :좌표 : 위도 : 36.628825506703954, 경도 : 127.45738760306085
# to 경도 : 127.45896785024753 or 100m
##########





