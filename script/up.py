from django_extensions.management.jobs import QuarterHourlyJob

from django.db import connection
import mysql.connector
from datetime import datetime, timedelta
import time as attendre

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from apps.app.models import Queue, QueueHist
from apps.app.models import AlertQueue, AlertQueueHist, AlertConfig

class Job(QuarterHourlyJob):
    help = "Script d'alerte ! en 15 min"

    def execute(self):
        
        datetimes = datetime.now()
        datetimes = datetimes.strftime("%Y-%m-%d %H:%M:%S")
        AlertConfig.objects.filter(params='last_verification').update(values=datetimes)

        """ La date et l'heure """
        time_in = "00:00:00"
        time_su = "23:59:59"
        datetime_today = datetime.now()
        datetime_yesterday = datetime.now()-timedelta(1)
        date_today = datetime_today.strftime("%Y-%m-%d")
        date_yesterday = datetime_yesterday.strftime("%Y-%m-%d")
        datetime_min = date_yesterday+" "+time_in
        datetime_max = date_today+" "+time_su

        """ Connexion à la base topup """
        try:
            
            mydb = mysql.connector.connect(
                host="10.39.231.23",
                user="ABOKOR",
                password="Abk_2021",
                database="TOPUPDJIB"
            )

            mycursor = mydb.cursor()

            """ Requete prod """
            #mycursor.execute("Select * from queue Where created_date BETWEEN '2021-06-01 00:00:00' AND '2049-12-31 23:59:59';")
            mycursor.execute("Select * from queue Where created_date BETWEEN '"+datetime_min+"' AND '"+datetime_max+"';")
            tab_queue = mycursor.fetchall()

            #mycursor.execute("Select * from queue_hist Where created_date BETWEEN '2021-06-01 00:00:00' AND '2049-12-31 23:59:59';")
            mycursor.execute("Select * from queue_hist Where created_date BETWEEN '"+datetime_min+"' AND '"+datetime_max+"';")
            tab_queue_hist = mycursor.fetchall()

            mycursor.close()

            mydb.close()

            # Historique
            ###################
            connection_status = AlertConfig.objects.get(params='connection_status')
            if connection_status.values=='KO':
                AlertConfig.objects.filter(params='connection_status').update(values="OK")

        except mysql.connector.Error as err:

            # Historique
            ###################
            AlertConfig.objects.filter(params='connection_status').update(values="KO")
        
        
        for x in tab_queue:
            
            id_queue = int(x[0])
            itemExistOnQueue = Queue.objects.filter(id_queue=id_queue).exists()
            itemExistOnErrorQueue = AlertQueue.objects.filter(id_queue=id_queue).exists()
            
            if itemExistOnQueue==False and itemExistOnErrorQueue==False:
                
                # Vérification de la provenance
                ERROR_ACTION_TYPE = False
                if x[1]== '44' or x[1]== '55':
                    ERROR_ACTION_TYPE = True

                # Vérification de la commande
                ERROR_COMMAND_CONTENT = False
                if x[2]==None:
                    ERROR_COMMAND_CONTENT = True

                # Vérification du numéros MSISDN
                ERROR_MSISDN = False
                if x[6]==None:
                    ERROR_MSISDN = True

                # Vérification du message d'erreur
                ERROR_DESCRIPTION = False
                if x[9]=='':
                    ERROR_DESCRIPTION = True
                
                # Vérification de l etat
                ERROR_ETAT = False
                if x[10]!='E' or x[10]==None:
                    ERROR_ETAT = True

                # Vérification du Thread_name
                ERROR_THREAD_NAME = False
                if x[11]==None:
                    ERROR_THREAD_NAME = True

                if ERROR_ACTION_TYPE or ERROR_COMMAND_CONTENT or ERROR_MSISDN or ERROR_DESCRIPTION or ERROR_ETAT or ERROR_THREAD_NAME:
                    alert_queue = AlertQueue.objects.create(
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
                        thread_number=x[12]
                    )
                    alert_queue.save()
                else:
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
                        thread_number=x[12]
                    )
                    queue.save()

        for y in tab_queue_hist:
            
            id_queue_hist = int(y[0])
            itemExistOnQueueHist = QueueHist.objects.filter(id_queue_hist=id_queue_hist).exists()
            itemExistOnErrorQueueHist = AlertQueueHist.objects.filter(id_queue_hist=id_queue_hist).exists()
            
            if itemExistOnQueueHist==False and itemExistOnErrorQueueHist==False:
                
                # Vérification de la commande
                ERROR_COMMAND_CONTENT = False
                if y[2]==None:
                    ERROR_COMMAND_CONTENT = True
                
                # Vérification du message d'erreur
                ERROR_DESCRIPTION = False
                if y[6]!='Opération effectué avec success !!!':
                    ERROR_DESCRIPTION = True

                # Vérification du numéros MSISDN
                ERROR_MSISDN = False
                if y[7]==None:
                    ERROR_MSISDN = True

                ERROR_ETAT = False
                if y[10]!='S' or y[10]==None:
                    ERROR_ETAT = True

                # Vérification du Thread_name
                ERROR_THREAD_NAME = False
                if y[11]==None:
                    ERROR_THREAD_NAME = True

                if ERROR_COMMAND_CONTENT or ERROR_DESCRIPTION or ERROR_MSISDN or ERROR_ETAT or ERROR_THREAD_NAME:
                    alert_queue_hist = AlertQueueHist.objects.create(
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
                        thread_number=y[12]
                    )
                    alert_queue_hist.save()
                else:
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
                        thread_number=y[12]
                    )
                    queue_hist.save()

        """ Etape 2) Traitement des erreurs """

        sec = 60

        alert_queue = AlertQueue.objects.filter(check_3=False)
        alert_queue_hist = AlertQueueHist.objects.filter(check_3=False)

        if alert_queue.exists() or alert_queue_hist.exists():
            for x in range(3):
                
                attendre.sleep(sec)
        
                try:
                    """ db connection """
                    mydb = mysql.connector.connect(
                        host="10.39.231.23",
                        user="ABOKOR",
                        password="Abk_2021",
                        database="TOPUPDJIB"
                    )

                    mycursor = mydb.cursor()

                    """ Requete prod """
                    #mycursor.execute("Select * from queue Where created_date BETWEEN '2021-06-01 00:00:00' AND '2049-12-31 23:59:59';")
                    mycursor.execute("Select * from queue Where created_date BETWEEN '"+datetime_min+"' AND '"+datetime_max+"';")
                    tab_queue = mycursor.fetchall()

                    #mycursor.execute("Select * from queue_hist Where created_date BETWEEN '2021-06-01 00:00:00' AND '2049-12-31 23:59:59';")
                    mycursor.execute("Select * from queue_hist Where created_date BETWEEN '"+datetime_min+"' AND '"+datetime_max+"';")
                    tab_queue_hist = mycursor.fetchall()

                    mycursor.close()

                    mydb.close()

                    if alert_queue_hist.exists():
                        for x in alert_queue_hist:
                    
                            for y in tab_queue_hist:        

                                if x.id_queue_hist==y[0]:

                                    obj = AlertQueueHist.objects.get(id_queue_hist=y[0])
                                    if obj.check_1 == False:
                                        AlertQueueHist.objects.filter(id_queue_hist=y[0]).update(check_1=True)
                                    else:
                                        if obj.check_2 == False:
                                            AlertQueueHist.objects.filter(id_queue_hist=y[0]).update(check_2=True)
                                        else:
                                            AlertQueueHist.objects.filter(id_queue_hist=y[0]).update(check_3=True)

                    if alert_queue.exists():
                        for x in alert_queue:
                    
                            find = 0

                            for y in tab_queue:        

                                if x.id_queue==y[0]:

                                    find = 1

                                    obj = AlertQueue.objects.get(id_queue=y[0])
                                    if obj.check_1 == False:
                                        AlertQueue.objects.filter(id_queue=y[0]).update(check_1=True)
                                    else:
                                        if obj.check_2 == False:
                                            AlertQueue.objects.filter(id_queue=y[0]).update(check_2=True)
                                        else:
                                            AlertQueue.objects.filter(id_queue=y[0]).update(check_3=True)
                            
                            if find==0:

                                AlertQueue.objects.filter(id_queue=x.id_queue).delete()

                except mysql.connector.Error as err:
                    
                    # Historique
                    ###################
                    AlertConfig.objects.filter(params='connection_status').update(values="KO")

                alert_queue = AlertQueue.objects.filter(check_3=False)
                alert_queue_hist = AlertQueueHist.objects.filter(check_3=False)

        """ Etape 3)  Signalement des erreurs """
        send_sms = AlertConfig.objects.get(params='send_sms')
        send_email = AlertConfig.objects.get(params='send_email')

        connection_status = AlertConfig.objects.get(params='connection_status')
        last_verification = AlertConfig.objects.get(params='last_verification')
        alert_queue = AlertQueue.objects.filter(check_1=True,check_2=True,check_3=True,reported=False,corrected=False).exists()
        
        code_12 = AlertQueue.objects.filter(check_1=True,check_2=True,check_3=True,reported=False,corrected=False,etat='N').count()
        code_13 = AlertQueue.objects.filter(check_1=True,check_2=True,check_3=True,reported=False,corrected=False,etat='OO').count()
        code_11 = AlertQueue.objects.filter(check_1=True,check_2=True,check_3=True,reported=False,corrected=False).count()
        code_11 = code_11-(code_12+code_13)
        code_14 = AlertQueueHist.objects.filter(check_1=True,check_2=True,check_3=True,reported=False,corrected=False).count()

        alert_queue_hist = AlertQueueHist.objects.filter(check_1=True,check_2=True,check_3=True,reported=False,corrected=False).exists()

        if send_sms.values=='OK' and (alert_queue or alert_queue_hist or connection_status.values=='KO'):

            if connection_status.values == 'KO':
                print('SMS error connexion !!!')
            else:
                print('SMS error niveau TopUp !!!')
            AlertConfig.objects.filter(params='send_sms').update(values='KO')

        if send_email.values=='OK' and (alert_queue or alert_queue_hist or connection_status.values=='KO'):

            """ Variable email """
            # Set Global Variables
            gmail_user = 'abokor.ahmed.kadar.nour@gmail.com'
            gmail_password = 'Mail.gmail.abokor'
            # Create Email 
            mail_from = 'Abokor Ahmed-Kadar Nour'
            #mail_to = 'abdoulkader_osman@intnet.dj,abdillahi_sougueh@intnet.dj,ismael.mourad@intnet.dj,nagwa_issam@intnet.dj,mouna_zain@intnet.dj,abdek.housssein@gmail.com,dt.bss.abdifatah@gmail.com,miwsaban@gmail.com,abokor.ahmed.kadar@outlook.com'
            mail_to = 'ismael.mourad@intnet.dj,nagwa_issam@intnet.dj,mouna_zain@intnet.dj,abdek.housssein@gmail.com,dt.bss.abdifatah@gmail.com,miwsaban@gmail.com,abokor.ahmed.kadar@outlook.com'
            mail_subject = 'Monitoring System !'

            message = MIMEMultipart('alternative')
            message['Subject'] = mail_subject
            message['From'] = mail_from
            message['To'] = mail_to
            
            if connection_status.values == 'KO':
                
                mail_message_body = '''\
                Hi,

                Veuillez savoir que la plateforme de monitoring du TOPUP arrive pas à se connecter à cette dernière.
                
                Connection Status : %s
                Dernière vérification : %s

                Interface Web : 172.16.1.89

                Cordialement,

                Xana System
                ''' % (connection_status.values, last_verification.values)

            else:   
                
                mail_message_body = '''\
                Hi,

                Veuillez savoir que la plateforme de monitoring du TOPUP détecte des erreurs sur cette dernière.
                
                Connection Status : %s
                Dernière vérification : %s
                
                Listes des codes : 

                code 11 : %s
                code 12 : %s
                code 13 : %s
                code 14 : %s

                Interface Web : 172.16.1.89

                Cordialement,

                Xana System
                ''' % (connection_status.values, last_verification.values, code_11, code_12, code_13, code_14)

            message.attach(MIMEText(mail_message_body, 'plain'))
            # Sent Email
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(gmail_user, gmail_password)
            server.sendmail(mail_from,mail_to.split(","), message.as_string())
            server.close()
            
            alert_queue = AlertQueue.objects.filter(check_1=True,check_2=True,check_3=True,reported=False,corrected=False)
            alert_queue_hist = AlertQueueHist.objects.filter(check_1=True,check_2=True,check_3=True,reported=False,corrected=False)

            for x in alert_queue:

                AlertQueue.objects.filter(id_queue=x.id_queue).update(reported=True)

            for x in alert_queue_hist:

                AlertQueueHist.objects.filter(id_queue_hist=x.id_queue_hist).update(reported=True)

        pass