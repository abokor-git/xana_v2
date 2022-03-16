from django_extensions.management.jobs import MinutelyJob

import mysql.connector

from datetime import datetime

from apps.app.models import Logs
from apps.app.models import Queue, QueueHist

class Job(MinutelyJob):
    help = "Import TopUp request every 5 minutes"

    def execute(self):
        
        PROCESS_NUMBER = 1612

        """ La date et l'heure """
        datetime_today = datetime.now()
        datetime_now = datetime_today.strftime("%Y-%m-%d %H:%M:%S")
        datetime_min = "2021-06-01 00:00:00"
        datetime_max = "2049-12-31 23:59:59"

        try:
            
            mydb = mysql.connector.connect(
                host="10.39.231.23",
                user="ABOKOR",
                password="Abk_2021",
                database="TOPUPDJIB"
            )

            mycursor = mydb.cursor()

            mycursor.execute("Select * from queue Where created_date BETWEEN '"+datetime_min+"' AND '"+datetime_max+"';")
            tab_queue = mycursor.fetchall()

            mycursor.execute("Select * from queue_hist Where created_date BETWEEN '"+datetime_min+"' AND '"+datetime_max+"';")
            tab_queue_hist = mycursor.fetchall()

            mycursor.close()

            mydb.close()

            for x in tab_queue:
            
                id_queue = int(x[0])
                itemExistOnQueue = Queue.objects.filter(id_queue=id_queue).exists()

                if itemExistOnQueue==False:

                    queue = Queue.objects.create(
                        id_queue=x[0],
                        action_type=x[1],
                        command_content=x[2],
                        created_date=x[3],
                        status=x[4],
                        updated_date=x[5],
                        msisdn=x[6],
                        pincode=x[7],
                        error_code=x[8],
                        error_description=x[9],
                        etat=x[10],
                        thread_name=x[11],
                        thread_number=x[12],
                        fee=x[13],
                        ip_adresse_client=x[14],
                        username=x[15]
                    )
                    queue.save()

            for y in tab_queue_hist:
            
                id_queue_hist = int(y[0])
                itemExistOnQueueHist = QueueHist.objects.filter(id_queue_hist=id_queue_hist).exists()
                
                if itemExistOnQueueHist==False:

                    queue_hist = QueueHist.objects.create(
                        id_queue_hist=y[0],
                        action_type=y[1],
                        command_content=y[2],
                        created_date=y[3],
                        status=y[4],
                        updated_date=y[5],
                        error_description=y[6],
                        msisdn=y[7],
                        pincode=y[8],
                        error_code=y[9],
                        etat=y[10],
                        thread_name=y[11],
                        thread_number=y[12],
                        fee=y[13],
                        ip_adresse_client=y[14],
                        username=y[15]
                    )
                    queue_hist.save()

            itemQueue = Queue.objects.filter(created_date__range=[datetime_min,datetime_max])

            for x in itemQueue:
                trouver = False
                for y in tab_queue:
                    if x.id_queue == y[0]:
                        trouver = True
                        if ( x.action_type != y[1] or x.command_content != y[2] or x.created_date != y[3] or x.status != y[4] or x.updated_date != y[5] or x.msisdn != y[6] or x.pincode != y[7] or x.error_code != y[8] or x.error_description != y[9] or x.etat != y[10] or x.thread_name != y[11] or x.thread_number != y[12] or x.fee != y[13] or x.ip_adresse_client != y[14] or x.username != y[15] ):
                            Queue.objects.filter(id_queue=x.id_queue).update(action_type=y[1],command_content=y[2],created_date=y[3],status=y[4],updated_date=y[5],msisdn=y[6],pincode=y[7],error_code=y[8],error_description=y[9],etat=y[10],thread_name=y[11],thread_number=y[12],fee=y[13],ip_adresse_client=y[14],username=y[15])
                if trouver == False:
                    print("delete items")
                    Queue.objects.filter(id_queue=x.id_queue).delete()

            message = "TopUp database reachable and saving complete"
            etat = "S"
            Logs.objects.create(date_time=datetime_now,process=PROCESS_NUMBER,message_description=message,etat=etat)

        except mysql.connector.Error as err:

            message = "Error TopUp database unreachable"
            etat = "E"
            Logs.objects.create(date_time=datetime_now,process=PROCESS_NUMBER,message_description=message,etat=etat)

        pass
