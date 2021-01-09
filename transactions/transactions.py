#!/usr/bin/env python3

import mysql.connector
import datetime

conn = mysql.connector.connect(
    host='localhost',
    database='dw',
    user='banebo',
    password='7298'
)
print("[+] Connected to db...")
conn.autocommit = False
cursor = conn.cursor(buffered=True)


def continents():
    q1 = 'SELECT * FROM dw.Continent'
    q2 = 'INSERT INTO dw.dw_continent (id_continent, name) VALUES (%s, %s)'
    cursor.execute(q1)
    res = cursor.fetchall()

    for c in res:
        try:
            cursor.execute(q2, (c[0], c[1]))
            conn.commit()
        except mysql.connector.Error as error:
            conn.rollback()
            print("Error occured: %s" % error)


def country():
    q1 = 'SELECT idCountry, country_name, idContinent FROM dw.Country'
    q2 = 'INSERT INTO dw_country (id_country, country_name, id_continent) VALUES (%s, %s, %s)'
    cursor.execute(q1)
    res = cursor.fetchall()

    for c in res:
        try:
            cursor.execute(q2, (c[0], c[1], c[2]))
            conn.commit()
        except mysql.connector.Error as err:
            conn.rollback()
            print("Error: %s" % err)


def city():
    q1 = 'SELECT idCity, idCountry, city_name FROM City'
    q2 = 'INSERT INTO dw_city (id_city, id_country, city_name) VALUES (%s, %s, %s)'
    cursor.execute(q1)
    res = cursor.fetchall()

    for c in res:
        try:
            cursor.execute(q2, (c[0], c[1], c[2]))
            conn.commit()
        except mysql.connector.Error as err:
            conn.rollback()
            print("Error: %s" % err)


def airport():
    q1 = 'SELECT idAirport, idCity, airport_name FROM Airport'
    q2 = 'INSERT INTO dw_airport (id_airport, id_city, airport_name) VALUES (%s, %s, %s)'
    cursor.execute(q1)
    res = cursor.fetchall()

    for a in res:
        try:
            cursor.execute(q2, (a[0], a[1], a[2]))
            conn.commit()
        except mysql.connector.Error as err:
            conn.rollback()
            print("Error: %s" % err)


def aircraft():
    q1 = 'SELECT idAircraft, aircraft_name FROM Aircraft'
    q2 = 'INSERT INTO dw_aircraft (id_aircraft, aircraft_name) VALUES (%s, %s)'
    cursor.execute(q1)
    res = cursor.fetchall()

    for a in res:
        try:
            cursor.execute(q2, (a[0], a[1]))
            conn.commit()
        except mysql.connector.Error as err:
            conn.rollback()
            print("Error: %s" % err)


def airline():
    q1 = 'SELECT idAirline, airline_name FROM Airline'
    q2 = 'INSERT INTO dw_airline (id_airline, airline_name) VALUES (%s, %s)'
    cursor.execute(q1)
    res = cursor.fetchall()

    for a in res:
        try:
            cursor.execute(q2, (a[0], a[1]))
            conn.commit()
        except mysql.connector.Error as err:
            conn.rollback()
            print("Error: %s" % err)


def time():
    q1 = 'SELECT dt_of_departure, dt_of_arrival FROM Flight'
    q2 = 'INSERT INTO dw_time (minute, hour, day, month, year) VALUES (%s, %s, %s, %s, %s)'
    cursor.execute(q1)
    tmp = cursor.fetchall()

    res = set()
    for i in tmp:
        for j in i:
            if j:
                res.add(j)

    n = 0
    for i in res:
        try:
            vals = (i.minute, i.hour, i.day, i.month, i.year)
            cursor.execute(q2, vals)
            conn.commit()
            print('[*] Status: %i/%i' % (n, len(res)), end='\r')
            n += 1
        except mysql.connector.Error as err:
            conn.rollback()
            print("Error: %s" % err)


def facts():
    print("[*] Fetching Flights...")
    q_dt = "SELECT idFlight, dt_of_departure, dt_of_arrival, idRoute FROM Flight"
    cursor.execute(q_dt)
    tmp = cursor.fetchall()
    flights = set()
    for i in tmp:
        if i[0] and i[1]:
            flights.add(i)
    print("[+] Done\n")

    q_dw_time = "SELECT id_time " + \
                "FROM dw_time dw_t " + \
                "WHERE dw_t.minute = %s " + \
                "AND dw_t.hour = %s " + \
                "AND dw_t.day = %s " + \
                "AND dw_t.month = %s " + \
                "AND dw_t.year = %s"
    q_route = "SELECT idAirline, id_src_airport, id_dst_airport " + \
              "FROM Route r " + \
              "WHERE r.idRoute = %d"
    q_aircraft = "SELECT idAircraft " + \
                 "FROM Route_has_Aircraft " + \
                 "WHERE idRoute = %s"
    q_tickets = "SELECT COUNT(idTicket) " + \
                "FROM Ticket " + \
                "WHERE idFlight = %s"
    q_fact = "INSERT INTO dw_facts (departure_time, arrival_time, aircraft, airline, id_src_airport, id_dst_airport, tickets)" + \
             "VALUES(%s, %s, %s, %s, %s, %s, %s)"

    print("[*] Starting insertion...")
    n = 1
    total = len(flights)
    for flight in flights:
        dept = flight[1]  # departure time
        arrt = flight[2]  # arrival time
        cursor.execute(q_dw_time, (dept.minute,
                                   dept.hour,
                                   dept.day,
                                   dept.month,
                                   dept.year))
        dw_dept_id = cursor.fetchone()[0]
        cursor.execute(q_dw_time, (arrt.minute,
                                   arrt.hour,
                                   arrt.day,
                                   arrt.month,
                                   arrt.year))
        dw_arrt_id = cursor.fetchone()[0]
        route_id = flight[3]
        cursor.execute(q_route % route_id)
        route = cursor.fetchone()
        airline_id = route[0]
        src_airport_id = route[1]
        dst_airport_id = route[2]
        cursor.execute(q_aircraft % route_id)
        aircraft_id = cursor.fetchone()[0]
        cursor.execute(q_tickets % flight[0])
        tickets = cursor.fetchone()[0]

        try:
            cursor.execute(q_fact % (dw_dept_id,
                                    dw_arrt_id,
                                    aircraft_id,
                                    airline_id,
                                    src_airport_id,
                                    dst_airport_id,
                                    tickets))
            print('[*] Status: %i / %i' % (n, total), end='\r')
            n += 1
            conn.commit()
        except mysql.connector.Error as err:
            print("[-] Error: %s" % err)
            conn.rollback()


def main():
    # continents()
    # country()
    # city()
    # airport()
    # aircraft()
    # airline()
    # time()
    # facts()


if __name__ == "__main__":
    main()
