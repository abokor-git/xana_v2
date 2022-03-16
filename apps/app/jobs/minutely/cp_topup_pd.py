from django_extensions.management.jobs import MinutelyJob

import mysql.connector

from datetime import datetime, timedelta

from apps.app.models import Logs
from apps.app.models import PackageData

class Job(MinutelyJob):
    help = "Import TopUp package_data"

    def execute(self):
        
        PROCESS_NUMBER = 1610

        """ La date et l'heure """
        time_in = "00:00:00"
        time_su = "23:59:59"
        datetime_today = datetime.now()
        datetime_yesterday = datetime.now()-timedelta(1)
        date_today = datetime_today.strftime("%Y-%m-%d")
        date_yesterday = datetime_yesterday.strftime("%Y-%m-%d")
        datetime_now = datetime_today.strftime("%Y-%m-%d %H:%M:%S")
        datetime_min = date_yesterday+" "+time_in
        datetime_max = date_today+" "+time_su

        PackageData.objects.all().delete()

        try:
            
            mydb = mysql.connector.connect(
                host="10.39.231.23",
                user="ABOKOR",
                password="Abk_2021",
                database="TOPUPDJIB"
            )

            mycursor = mydb.cursor()

            mycursor.execute("Select * from package_data;")
            tab_package_data = mycursor.fetchall()

            mycursor.close()

            mydb.close()

            for x in tab_package_data:
                PackageData.objects.create(
                    id_package_date = x[0],
                    balance_data = x[1],
                    code = x[2],
                    created_date = x[3],
                    frais = x[4],
                    promotion1 = x[5],
                    promotion1_data = x[6],
                    promotion2 = x[7],
                    promotion2_data = x[8],
                    promotion3 = x[9],
                    promotion3_data = x[10],
                    promotion4 = x[11],
                    promotion4_data = x[12],
                    promotion5 = x[13],
                    promotion5_data = x[14],
                    quantite_data = x[15],
                    updated_date = x[16],
                    validite = x[17],
                    description = x[18],
                    balance_voix = x[19],
                    quantite_voix = x[20],
                    types = x[21],
                    fraisrg = x[22],
                )

            message = "TopUp database reachable and saving complete"
            etat = "S"
            Logs.objects.create(date_time=datetime_now,process=PROCESS_NUMBER,message_description=message,etat=etat)

        except mysql.connector.Error as err:

            message = "Error TopUp database unreachable"
            etat = "E"
            Logs.objects.create(date_time=datetime_now,process=PROCESS_NUMBER,message_description=message,etat=etat)

        pass
