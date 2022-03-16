from django_extensions.management.jobs import HourlyJob

import requests

import sqlite3

class Job(HourlyJob):
    help = "My ygo job."

    def execute(self):

        url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

        try:

            sqliteConnection = sqlite3.connect('cards.cdb')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            sqlite_select_query = """SELECT * from texts"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            print("Total rows are:  ", len(records))
            print("Printing each row")
            for row in records:

                if row[0]>10705656:

                    print("###############################################")
                    print("Id: ", row[0])
                    #print("Name: ", row[1])
                    #print("Desc EN: ", row[2])

                    querystring = {"id":str(row[0]),"language":"fr"}

                    headers = {"Content-Type": "application/json"}

                    response = requests.request("POST", url, headers=headers, params=querystring)

                    #print("Name Fr: "+str(response.json()["data"][0]["name"]))
                    #print("Desc FR: "+str(response.json()["data"][0]["desc"]))
                    print("###############################################")

                    try:
                        sql_update_query = """Update texts set name = ?, desc = ? where id = ?"""
                        data = (str(response.json()["data"][0]["name"]), str(response.json()["data"][0]["desc"]), row[0])
                        cursor.execute(sql_update_query, data)
                        sqliteConnection.commit()
                        print("Record Updated successfully")
                    except KeyError:
                        print("pass")

                    print("###############################################")

                    cursor.close()

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("The SQLite connection is closed")

        pass
