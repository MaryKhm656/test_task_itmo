from math import radians, sin, cos, atan2, sqrt
from pathlib import Path


def read_zip_all():
    i = 0
    header = []
    zip_codes = []
    root_dir = Path(__file__).parent.parent.parent
    csv_path = root_dir / 'zip_codes_states.csv'
    for line in open(csv_path).read().split("\n"):
        skip_line = False
        m = line.strip().replace('"', '').split(",")
        i += 1
        if i == 1:
            for val in m:
                header.append(val)
        else:
            zip_data = []
            for idx in range(0, len(m)):
                if m[idx] == '':
                    skip_line = True
                    break
                if header[idx] == "latitude" or header[idx] == "longitude":
                    val = float(m[idx])
                else:
                    val = m[idx]
                zip_data.append(val)
            if not skip_line:
                zip_codes.append(zip_data)
    return zip_codes


def get_coordinates_by_zip(zip_code: str, all_zip: list):

    for row in all_zip:
        if row[0] == zip_code:
            return float(row[1]), float(row[2])
    return None, None

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 3958.8
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)

    a = sin(dphi/2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda*2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c