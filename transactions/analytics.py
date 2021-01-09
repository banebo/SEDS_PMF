#!/usr/bin/env python3

from matplotlib import pyplot as plt
import numpy as np
import texttable
import mysql.connector as mysql

conn = mysql.connect(
                     host="localhost",
                     database="dw",
                     user="banebo",
                     password="7298"
                    )

cursor = conn.cursor()

# most used aircraft
q1 = """
        SELECT aircraft, aircraft_name, MAX(c) AS total_flights
        FROM (
            SELECT aircraft, aircraft_name, COUNT(aircraft) AS c
            FROM dw_facts f, dw_aircraft a
            WHERE f.aircraft = a.id_aircraft
            GROUP BY aircraft
        ) AS tmp
     """

cursor.execute(q1)
a = cursor.fetchone()
t = texttable.Texttable()
t.add_rows([['ID', 'Aircraft Name', 'Total Flights'], list(a)])
print('q1:')
print(t.draw())


q2 = """
        SELECT airline,airline_name, MAX(total)
        FROM (
            SELECT airline, airline_name, COUNT(*) as total
            FROM dw_facts f, dw_airline a
            WHERE f.airline = a.id_airline AND
                (
                    SELECT continent.id_continent
                    FROM dw_airport airport, dw_city city, dw_country country, dw_continent continent
                    WHERE f.id_src_airport = airport.id_airport AND
                        airport.id_city = city.id_city AND
                        city.id_country = country.id_country AND
                        country.id_continent = continent.id_continent
                )
                !=
                (
                    SELECT continent.id_continent
                    FROM dw_airport airport, dw_city city, dw_country country, dw_continent continent
                    WHERE f.id_dst_airport = airport.id_airport AND
                        airport.id_city = city.id_city AND
                        city.id_country = country.id_country AND
                        country.id_continent = continent.id_continent
                )
            GROUP BY airline
            ORDER BY total DESC
            ) AS t
     """

cursor.execute(q2)
res = cursor.fetchall()
print("\n\nq2:")
t = texttable.Texttable()
t.add_row(['ID', 'Airline Name', 'Total'])
for i in res:
    t.add_row(i)
print(t.draw())


q3 = """
        SELECT SUM(tickets) AS total_tickets
        FROM dw_facts f, dw_time t
        WHERE f.arrival_time = t.id_time AND t.month = %s AND t.year = %s
     """

m = int(input('\n[?] Enter month: '))
y= int(input("year: "))
cursor.execute(q3 % (m, y))
res = cursor.fetchone()
print("[*] Total number of tickets sold in month %d is: %d" % (m, res[0]))

#############################################################################

# graficki prikaz karata po mesecu u odredjenoj godini
qn = '''
        SELECT SUM(tickets) AS total
        FROM dw_facts f, dw_time t
        WHERE f.arrival_time = t.id_time AND
              t.month = %d AND
              t.year = %d
     '''

data = []
year = int(input('\n[?] Enter year: '))
for i in range(1, 13):
    cursor.execute(qn % (i, year))
    data.append(cursor.fetchone()[0])
print(data)
y_pos = [1,2,3,4,5,6,7,8,9,10,11,12]
plt.ylabel("Kolicina prodatih karata")
plt.xlabel("Mesec u godini")
plt.bar(y_pos, data)
plt.show()



    