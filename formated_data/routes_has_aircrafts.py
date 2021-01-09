#!/usr/bin/env python3


def get_airports():
    with open('./airports.csv', 'r') as file:
        data = file.readlines()
    data.pop(0)
    airports = []
    for a in data:
        l = a.split(',')
        id = l[0]
        name = l[1]
        iata = l[2]
        icao = l[3]
        airports.append({'id': id, 'name': name, 'iata': iata, 'icao': icao})
    return airports


def get_aircrafts():
    with open('./aircraft.csv', 'r') as file:
        data = file.readlines()
    data.pop(0)
    planes = []
    for i in data:
        l = i.strip('\n').split(',')
        id = l[0]
        iata = l[2]
        icao = l[3]
        planes.append({'id': id, 'iata': iata, 'icao': icao})
    return planes


def airport_exists(airports, id):
    for airport in airports:
        if airport['id'] == id:
            return True
    return False


def planes_exist(planes, codes):
    tmp = []
    for code in codes:
        for plane in planes:
            if plane['icao'] == code or \
               plane['iata'] == code:
                tmp.append(plane['id'])
    return tmp


def write_routes(path, out_path):
    with open(path, 'r') as file:
        routes = file.readlines()
    for i in range(4):
        routes.pop(0)
    airports = get_airports()
    planes = get_aircrafts()
    id = 1
    ret = []
    print("\n[*] Writing routes...")
    content = 'ID | ID_AIRLINE |ID_SRC_AIRPORT | ID_DST_AIRPORT\n'
    for line in routes:
        route = line.strip('\n').split(',')
        id_airline = route[1]
        id_src = route[3]
        id_dst = route[5]
        if len(route[8].split(' ')) != 0:
            aircrafts = planes_exist(planes, route[8].split(" "))
        else:
            continue
        if id_src == '\\N' or id_dst == '\\N':
            continue
        if not (airport_exists(airports, id_src) and
                airport_exists(airports, id_dst)):
            continue
        content += '%s,%s,%s,%s\n' % (id, id_airline, id_src, id_dst)
        ret.append({'id': id, 'id_src_airport': id_src,
                    'id_dst_airport': id_dst, 'aircrafts': aircrafts})
        id += 1
    with open(out_path, 'w') as file:
        file.writelines(content)
    print("[+] Done\n")
    return ret


def write_plane_route(routes, out_path):
    print("[*] Writing route_has_aircraft...")
    line = 'ID_ROUTE | ID_AIRCRAFT\n'
    for route in routes:
        for plane in route['aircrafts']:
            line += '%s,%s\n' % (route['id'], plane)
    with open(out_path, 'w') as file:
        file.writelines(line)
    print("[+] Done\n")


def main():
    routes_path = '../data/routes.dat'
    routes_w_path = './routes.csv'
    route_has_aircraft = './route_has_aircraft.csv'

    routes = write_routes(routes_path, routes_w_path)
    write_plane_route(routes, route_has_aircraft)


if __name__ == "__main__":
    main()
