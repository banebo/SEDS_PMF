#!/usr/bin/env python3

import random
import string


def get_routes(routes_path):
    with open(routes_path, 'r') as file:
        data = file.readlines()
    data.pop(0)
    routes = []
    for row in data:
        routes.append(row.strip("\n "))
    return routes


def get_date_time():
    year = random.randrange(1900, 2019)
    month = random.randrange(0, 12)
    seconds = '00'

    day_dep = str(random.randrange(1, 25))
    h_dep = str(random.randrange(1, 24))
    mins_dep = str(random.randrange(1, 59))

    day_arr = int(day_dep) + random.randrange(0, 1)
    h_arr = int(h_dep) + random.randrange(0, 24)
    mins_arr = int(mins_dep) + random.randrange(0, 59)

    if int(mins_arr) >= 60:
        h_arr = str(int(h_arr) + 1)
        mins_arr = '00'
    if int(h_arr) >= 24:
        day_arr = str(int(day_arr) + 1)
        h_arr = '00'

    # format
    day_dep = day_dep if int(day_dep) > 10 else '0' + str(day_dep)
    h_dep = h_dep if int(h_dep) > 10 else '0' + str(h_dep)
    mins_dep = mins_dep if int(mins_dep) > 10 else '0' + str(mins_dep)
    day_arr = day_arr if int(day_arr) > 10 else '0' + str(day_arr)
    h_arr = h_arr if int(h_arr) > 10 else '0' + str(h_arr)
    mins_arr = mins_arr if int(mins_arr) > 10 else '0' + str(mins_arr)

    dt_dep = '%.2s-%.2s-%.2s %.2s:%.2s:%.2s' % (year, month, day_dep, h_dep, mins_dep, seconds)
    dt_arr = '%.2s-%.2s-%.2s %.2s:%.2s:%.2s' % (year, month, day_arr, h_arr, mins_arr, seconds)

    return dt_dep, dt_arr


def get_flight_No():
    no = ''
    prefix = random.randrange(1, 3)
    for i in range(random.randrange(1, 3)):
        no += random.choice(string.ascii_uppercase)
    for i in range(random.randrange(3, 5)):
        no += str(random.randrange(0, 10))
    for i in range(random.randrange(0, 2)):
        no += random.choice(string.ascii_uppercase)
    return no


def write_flights(routes, out_path):
    lines = 'ID | DT_OF_DEPARTURE | DT_OF_ARIVAL | FLUGHT_NO | ID_ROUTE\n'
    # YYYY-MM-DD hh:mm:ss
    print("\n[*] Writing flights...")
    flights = []
    id = 1
    for i in range(200):
        for route_id in routes:
            dt_dep, dt_arrive = get_date_time()
            flight_no = get_flight_No()
            flights.append({'id': id+1, 'dt_departure': dt_dep,
                            'dt_arrival': dt_arrive, 'flight_no': flight_no,
                            'route_id': route_id})
            lines += '%s,%s,%s,%s,%s\n' % \
                    (str(id), dt_dep, dt_arrive, flight_no, route_id)
            id += 1
    with open(out_path, 'w') as file:
        file.writelines(lines)
    print("[+] Done\n")
    return flights


def main():
    routes = get_routes('./idRoutes.txt')
    flights = write_flights(routes, './flights.csv')




if __name__ == "__main__":
    main()