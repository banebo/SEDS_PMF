#!/usr/bin/env python3

def load_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines.pop(0)  # removemo the 1st line
    return lines

def extract(data):
    extracted = []
    for line in data:
        cols = line.split(',')
        id = cols[0]
        airport_name = cols[1].strip('"')
        city_name = cols[2].strip('"')
        country_name = cols[3].strip('"')
        iata = cols[4].strip('\\N"')
        icao = cols[5].strip('\\N"')
        time_zone = cols[9].strip('\\N')
        if city_name != '' and country_name != '':
            extracted.append({'id': id, 'airport_name': airport_name,
                              'country_name': country_name,
                              'city_name': city_name, 'iata': iata, 'icao': icao,
                              'time_zone': time_zone})
    return extracted


def get_country_id(countries, name):
    for c in countries:
        if c['name'] == name:
            return c['id']
    return ''


def city_exists(cities, city_name):
    for c in cities:
        if c['name'] == city_name:
            return True
    return False


def write_cities(data, countries_path, out_path):
    with open(countries_path, 'r') as file:
        countries = file.readlines()
    countries.pop(0)
    country_names = []
    for line in countries:
        l = line.split(',')
        country_names.append({'id': l[0], 'name': l[1]})
    cities = []
    id = 1
    line = "ID | NAME | TIME_ZONE | COUNTRY_ID\n"
    for i in data:
        city = {'id': id}
        city['name'] = i['city_name']
        city['time_zone'] = i['time_zone']
        city['country_id'] = get_country_id(country_names, i['country_name'])
        if not city_exists(cities, city['name']) and city['country_id'] != '':
            cities.append(city)
            id += 1
            line += "%s,%s,%s,%s\n" % (city['id'], city['name'],
                                       city['time_zone'], city['country_id'])
    with open(out_path, 'w') as file:
        file.writelines(line)
    return cities

def get_city_id(arr, name):
    for i in arr:
        if i['name'] == name:
            return i['id']
    return -1

def write_airports(data, cities, out_path):
    line = "ID | NAME | IATA(3) | ICAO(4) | CITY_ID\n"
    for airport in data:
        id = airport['id']
        name = airport['airport_name']
        iata = airport['iata']
        icao = airport['icao']
        id_city = get_city_id(cities, airport['city_name'])
        if id_city != -1:
            line += '%s,%s,%s,%s,%s\n' % (id, name, iata, icao, id_city)
    with open(out_path, 'w') as file:
        file.writelines(line)
    

def main():
    airports_path = '../data/airports.dat'
    countries_path = './countries.csv'
    cities_path = './cities.csv'
    airport_w_path = './airports.csv'

    print("\n[*] Loading data...")
    data = load_data(airports_path)
    data = extract(data)
    print("[+] Done\n")

    print('[*] Writing cities to %s' % cities_path)
    cities = write_cities(data, countries_path, cities_path)
    print('[+] Done\n')
    
    print('[*] Writing airports...')
    write_airports(data, cities, airport_w_path)
    print('[+] Done\n')

    
if __name__ == "__main__":
    main()
