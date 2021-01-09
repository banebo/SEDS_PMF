import random;

def continents():
    with open('../formated_data/continets.csv', 'r') as file:
        src = file.readlines()
    src.pop(0)

    txt = ''
    for l in src:
        h = l.strip('\n ').split(',')
        txt += 'INSERT INTO dw.Continent (idContinent, continent_name) VALUES (%s, "%s");\n' % (h[0], h[1])

    with open('./continents.sql', 'w') as file:
        file.writelines(txt)


def regions():
    with open('../formated_data/regions.csv', 'r') as file:
        s = file.readlines()
    s.pop(0)

    txt = ''
    for l in s:
        h = l.strip("\n ").split(',')
        txt += 'INSERT INTO dw.Region (idRegion, region_name) VALUES (%s, "%s");\n' % \
               (h[0], h[1])

    with open('./regions.sql', 'w') as file:
        file.writelines(txt)


def countries():
    with open('../formated_data/countries.csv') as file:
        src = file.readlines()
    src.pop(0)

    txt = ''
    for l in src:
        h = l.strip('\n ').split(',')
        for i in range(len(h)):
            if h[i] == '':
                h[i] = "NULL"
        txt += 'INSERT INTO dw.Country (idCountry, country_name, alpha_2, alpha_3, code, idContinent, idRegion) VALUES (%s, "%s", "%s", "%s", %s, %s, %s);\n' % \
               (h[0], h[1], h[2], h[3], h[4], h[5], h[6])

    with open('./countries.sql', 'w') as file:
        file.writelines(txt)


def cities():
    with open('../formated_data/cities.csv') as file:
        s = file.readlines()
    s.pop(0)

    txt = ''
    for l in s:
        h = l.strip('\n ').split(',')
        for i in range(len(h)):
            if h[i] == '':
                h[i] = "NULL"
        txt += 'INSERT INTO dw.City (idCity, city_name, time_zone, idCountry) VALUES (%s, "%s", %s, %s);\n' % \
               (h[0], h[1], h[2], h[3])

    with open('./cities.sql', 'w') as file:
        file.writelines(txt)
 

def airline():
    with open('../formated_data/airlines.csv', 'r') as file:
        s = file.readlines()
    s.pop(0)

    txt = ''
    for l in s:
        h = l.strip('\n ').split(',')
        if h[5] == '':
            h[5] = "NULL"
        if len(h[4]) >= 45:
            h[4] = ""
        txt += 'INSERT INTO dw.Airline (idAirline, airline_name, airline_IATA, airline_ICAO, callsign, country_of_origin) VALUES (%s, "%s", "%s", "%s", "%s", %s);\n' % \
                (h[0], h[1], h[2], h[3], h[4], h[5])

    with open('./airlines.sql', 'w') as file:
        file.writelines(txt)
 

def aircraft():
    with open('../formated_data/aircraft.csv', 'r') as file:
        s = file.readlines()
    s.pop(0)

    txt = ''
    for l in s:
        h = l.strip('\n ').split(',')
        txt += 'INSERT INTO dw.Aircraft (idAircraft, aircraft_name, aircraft_IATA, aircraft_ICAO) VALUES (%s, "%s", "%s", "%s");\n' % \
                (h[0], h[1], h[2], h[3])
    
    with open('./aircrafts.sql', 'w') as file:
        file.writelines(txt)


def airports():
    with open('../formated_data/airports.csv', 'r') as file:
        s = file.readlines()
    s.pop(0)
    txt = ''
    for l in s:
        h = l.strip('\n ').split(',')
        if h[4] == '':
            h[4] = "NULL"
        txt += 'INSERT INTO dw.Airport (idAirport, airport_name, airport_IATA, airport_ICAO, idCity) VALUES (%s, "%s", "%s", "%s", %s);\n' % \
                (h[0], h[1], h[2], h[3], h[4])
    
    with open('./airports.sql', 'w') as file:
        file.writelines(txt)

def people():
    with open('../formated_data/people.csv', 'r') as file:
        s = file.readlines()
    s.pop(0)
    txt = ''
    for l in s:
        h = l.strip('\n ').split(',')
        txt += 'INSERT INTO dw.Person (idPerson, person_name, person_surname) VALUES (%s, "%s", "%s");\n' % \
                (h[0], h[1], h[2])
    
    with open('./people.sql', 'w') as file:
        file.writelines(txt)


def routes():
    file_name = '../formated_data/routes.csv'
    with open(file_name, 'r') as file:
        lines = file.readlines()
    lines.pop(0)

    rnd_r = []
    # get random 30 routes
    for i in range(30):
        rnd = random.randint(0, len(lines))
        rnd_r.append(lines[rnd])

    txt = ''
    for r in rnd_r:
        data = r.strip(" \n").split(',')
        txt += 'INSERT INTO dw.Route(idRoute, idAirline, id_src_airport, id_dst_airport) VALUES (%s, %s, %s, %s); \n' % \
               (data[0], data[1], data[2], data[3])
    
    with open('./routes.sql', 'w') as file:
        file.writelines(txt)
    print('done')


def route_has_aircraft():
    with open('../formated_data/idRoutes.txt', 'r') as file:
        ids = file.readlines()
    ids.pop(0)
    
    with open('../formated_data/aircraft.csv') as file:
        airs = file.readlines()

    print('got %i planes' % len(airs))

    txt = ''
    for id in ids:
        # rnd 1 - 4 aircrafts
        count = random.randint(1, 4)
        rnd_airs = []
        for i in range(count):
            rnd = random.randint(0, len(airs)-1)
            tmp_a = airs[rnd]
            id_tmp = tmp_a.split(',')[0].strip(" ")
            rnd_airs.append(id_tmp)
        
        for a in rnd_airs:
            txt += 'INSERT INTO dw.Route_has_Aircraft(idRoute, idAircraft) VALUES(%s, %s);\n' \
                % (id.strip(" \n"), a)
            
    with open('./route_has_aircraft.sql', 'w') as file:
        file.writelines(txt)
    print("done")


def flights():
    with open('../formated_data/flights.csv') as file:
        flights = file.readlines()
    flights.pop(0)

    txt = ''
    for f in flights:
        d = f.strip('\n ').split(',')
        txt += 'INSERT INTO dw.Flight(idFlight, dt_of_departure, dt_of_arrival, flight_number, idRoute) VALUES(%s,"%s", "%s", "%s", %s);\n' \
               %(d[0], d[1], d[2], d[3], d[4])
    
    with open('./flights.sql', 'w') as file:
        file.writelines(txt)
    print('done')


def ticket():
    with open('../formated_data/flights.csv', 'r') as file:
        flights = file.readlines()
    flights.pop(0)

    txt = ''
    id = 0
    for flight in flights:
        idFlight = flight.split(',')[0].strip('\n ')
        for i in range(10):
            id += 1
            price = random.randrange(120, 1200)
            idPerson = random.randint(1, 1000)
            txt += 'INSERT INTO dw.Ticket(idTicket, price, idPerson, idFlight) VALUES(%s, %s, %s, %s);\n' % \
                   (id, price, idPerson, idFlight)
    
    with open('./tickets.sql', 'w') as file:
        file.writelines(txt)



def main():
    # continents()
    # print("[+] Wrote Continents")
    # regions()
    # print("[+] Wrote Regions")
    # countries()
    # print("[+] Wrote Countries")
    # cities()
    # print("[+] Wrote Cities")
    # airline()
    # print("[+] Wrote Airlines")
    # aircraft()
    # print("[+] Wrote Aircrafts")
    # airports()
    # print("[+] Wrote Airports")
    # people()
    # print("[+] Wrote People")
    # routes()
    # route_has_aircraft()
    # flights()
    ticket()


if __name__ == "__main__":
    main()
