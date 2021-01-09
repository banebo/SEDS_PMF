#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def extract_data(data):
    f = []
    for line, n in zip(data, range(len(data))):
        line = line.strip('\n ')
        cols = line.split(',')
        country = cols[0].strip()
        alpha2 = cols[1].strip()
        alpha3 = cols[2].strip()
        code = cols[3].strip()
        continent = cols[5].strip()
        region = cols[6]
        if continent == 'Americas':
            continent = 'America'
        if len(alpha2) != 2 or len(alpha3) != 3:
            print('[-] Error at line %d' % n)
        else:
            tmp = {'country': country, 'alpha2': alpha2,
                   'alpha3': alpha3, 'code': code,
                   'continent': continent, 'region': region}
            f.append(tmp)
    return f


def get_id(arr, string):
    for i in arr:
        if i['name'] == string:
            return i['id']
    return ''


def write_countries(data, file_path, continents, regions):
    lines = "ID | NAME | ALPHA-2 | ALPHA-3 | CODE | ID_CONTINENT | ID_REGION\n"
    id = 1
    for c in data:
        continent = c['continent']
        region = c['region']
        id_continent = get_id(continents, continent)
        id_region = get_id(regions, region)
        lines += "%d,%s,%2s,%3s,%s,%s,%s\n" % \
                 (id, c['country'], c['alpha2'], c['alpha3'], c['code'],
                  id_continent, id_region)
        id += 1
    with open(file_path, 'w') as file:
        file.writelines(lines)


def write_regions(data, file_path):
    lines = "ID | NAME\n"
    regions = set()
    for i in data:
        if i['region'] != '':
            regions.add(i['region'])
    id = 1
    ret = []
    for r in regions:
        lines += "%d,%s\n" % (id, r)
        ret.append({'id': id, 'name': r})
        id += 1
    with open(file_path, 'w') as file:
        file.writelines(lines)
    return ret


def write_continets(data, file_path):
    lines = "ID | NAME\n"
    continents = set()
    for i in data:
        continents.add(i['continent']) if i['continent'] != '' else None
    id = 1
    ret = []
    for c in continents:
        lines += "%d,%s\n" % (id, c)
        ret.append({'id': id, 'name': c})
        id += 1
    with open(file_path, 'w') as file:
        file.writelines(lines)
    return ret


def main():
    file_path = "../data/country_continent.csv"
    countries_path = 'countries.csv'
    continents_path = 'continets.csv'
    region_path = 'regions.csv'

    with open(file_path, 'r') as file:
        data = file.readlines()
    data.pop(0)  # skip first line
    extracted = extract_data(data)

    print("\n[*] Writing continents to %s" % continents_path)
    conts = write_continets(extracted, continents_path)
    print("[+] Done")

    print("\n[*] Writing regions to %s" % region_path)
    regions = write_regions(extracted, region_path)
    print("[+] Done")

    print("\n[*] Writing countries to %s" % countries_path)
    write_countries(extracted, countries_path, conts, regions)
    print("[+] Done")

    print('\n')


if __name__ == "__main__":
    main()
