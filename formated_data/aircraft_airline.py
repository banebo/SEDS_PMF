#!/usr/bin/env python3


def write_aircrafts(aircraft_path, aircraft_w_path):
    with open(aircraft_path, 'r') as file:
        data = file.readlines()
    data.pop(0)
    print("\n[*] Writing aircrafts...")
    line = 'ID | NAME | IATA(3) | ICAO(4)\n'
    id = 1
    for p in data:
        l = p.split(',')
        name = l[0].strip('"')
        iata = l[1].strip('"\\N')
        icao = l[2].strip('"\n\\N')
        line += '%d,%s,%s,%s\n' % (id, name, iata, icao)
        id += 1
    with open(aircraft_w_path, 'w') as file:
        file.writelines(line)
    print('[+] Done\n')


def get_country_id(name):
    with open('./countries.csv', 'r') as file:
        tmp_countries = file.readlines()
    tmp_countries.pop(0)
    for c in tmp_countries:
        l = c.split(',')
        if l[1] == name:
            return l[0]
    return -1


def write_airlines(airlines_path, airlines_w_path):
    with open(airlines_path, 'r') as file:
        data = file.readlines()
    data.pop(0)
    print("[*] Writing airlines...")
    line = 'ID | NAME | IATA(3) | ICAO(4) | CALLSIGN | ID_COUNTRY_OF_ORIGIN\n'
    for a in data:
        l = a.split(',')
        id = l[0]
        name = l[1].strip('"')
        iata = l[3].strip('"\\N?!')
        icao = l[4].strip('"\\N?!')
        callsign = l[5].strip('"\\N')
        country_id = get_country_id(l[6].strip('"\\N'))
        if country_id == -1:
            country_id = ''
        if id != '' and name != '':
            line += '%s,%s,%s,%s,%s,%s\n' % (id, name, iata,
                                             icao, callsign, country_id)
    with open(airlines_w_path, 'w') as file:
        file.writelines(line)
    print("[+] Done\n")


def main():
    aircraft_path = '../data/planes.dat'
    aircraft_w_path = './aircraft.csv'
    airlines_path = '../data/airlines.dat'
    airlines_w_path = './airlines.csv'

    write_aircrafts(aircraft_path, aircraft_w_path)
    write_airlines(airlines_path, airlines_w_path)


if __name__ == "__main__":
    main()
