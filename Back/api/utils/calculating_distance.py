from geopy import distance

wellington = (-41.32, 174.81)
salamanca = (0, 0)


def calculate_distance(longitude_1, latitude_1, longitude_2, latitude_2):
    point_1 = [float(str(latitude_1)), float(str(longitude_1))]
    point_2 = [float(str(latitude_2)), float(str(longitude_2))]
    return distance.distance(point_1, point_2).km
