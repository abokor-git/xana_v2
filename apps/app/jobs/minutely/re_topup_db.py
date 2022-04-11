from re import A
from tabnanny import check
from django_extensions.management.jobs import MinutelyJob

from datetime import datetime

from apps.app.models import Logs, Queue, QueueHist
from apps.app.models import AlertQueue, AlertQueueHist

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Job(MinutelyJob):
    help = "report errors with gmail every 2 minutes"

    def execute(self):

        PROCESS_NUMBER = 1614

        """ La date et l'heure """
        datetime_today = datetime.now()
        datetime_now = datetime_today.strftime("%Y-%m-%d %H:%M:%S")

        found = False

        tab_queue = AlertQueue.objects.filter(check_1=True,check_2=True,check_3=True,reported=False)
        tab_queuehist = AlertQueueHist.objects.filter(check_1=True,check_2=True,check_3=True,reported=False)

        ###################################################################

        if tab_queue.count() != 0 or tab_queuehist.count() != 0:

            found = True

            if tab_queue.count() == 0:
                alert_queue = "Aucune erreur dans la table Queue"
            else:
                alert_queue = """\

                    <p>Table Queue :</p>

                    <table> 
                        <tr>
                            <th>action_type</th>
                            <th>command_content</th>
                            <th>created_date</th>
                            <th>status</th>
                            <th>updated_date</th>
                            <th>msisdn</th>
                            <th>pincode</th>
                            <th>error_code</th>
                            <th>error_description</th>
                            <th>etat</th>
                            <th>thread_name</th>
                            <th>thread_number</th>
                            <th>fee</th>
                            <th>ip_adresse_client</th>
                            <th>username</th>
                        </tr>
                    """

                for x in tab_queue:
                    AlertQueue.objects.filter(id=x.id).update(reported=True)
                    item_queue = x.id_queue
                    item = """\
                        <tr>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                        </tr>
                        """ % (item_queue.action_type,
                        item_queue.command_content,
                        item_queue.created_date,
                        item_queue.status,
                        item_queue.updated_date,
                        item_queue.msisdn,
                        item_queue.pincode,
                        item_queue.error_code,
                        item_queue.error_description,
                        item_queue.etat,
                        item_queue.thread_name,
                        item_queue.thread_number,
                        item_queue.fee,
                        item_queue.ip_adresse_client,
                        item_queue.username,
                        )
                    
                    alert_queue = alert_queue+item
                
                alert_queue = alert_queue + """\
                        </table>
                    """

            ###########

            if tab_queuehist.count() == 0:
                alert_queue_hist = "Aucune erreur dans la table QueueHist"
            else:
                alert_queue_hist = """\

                    <p>Table QueueHist :</p>

                    <table> 
                        <tr>
                            <th>action_type</th>
                            <th>command_content</th>
                            <th>created_date</th>
                            <th>status</th>
                            <th>updated_date</th>
                            <th>msisdn</th>
                            <th>pincode</th>
                            <th>error_code</th>
                            <th>error_description</th>
                            <th>etat</th>
                            <th>thread_name</th>
                            <th>thread_number</th>
                            <th>fee</th>
                            <th>ip_adresse_client</th>
                            <th>username</th>
                        </tr>
                    """

                for y in tab_queuehist:
                    AlertQueueHist.objects.filter(id=y.id).update(reported=True)
                    item_queue_hist = y.id_queue_hist
                    item = """\
                        <tr>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                        </tr>
                        """ % (item_queue_hist.action_type,
                        item_queue_hist.command_content,
                        item_queue_hist.created_date,
                        item_queue_hist.status,
                        item_queue_hist.updated_date,
                        item_queue_hist.msisdn,
                        item_queue_hist.pincode,
                        item_queue_hist.error_code,
                        item_queue_hist.error_description,
                        item_queue_hist.etat,
                        item_queue_hist.thread_name,
                        item_queue_hist.thread_number,
                        item_queue_hist.fee,
                        item_queue_hist.ip_adresse_client,
                        item_queue_hist.username,
                        )
                    
                    alert_queue_hist = alert_queue_hist+item
                
                alert_queue_hist = alert_queue_hist + """\
                        </table>
                    """

            link = "http://172.16.1.89/"

            ###################################################################

            """ Variable email """
            # Set Global Variables
            gmail_user = 'xana.system.v2@outlook.com'
            gmail_password = 'Xana_v2_system'
            # Create Email 
            mail_from = 'Xana System'
            #mail_to = 'nagwa_issam@intnet.dj,mouna_zain@intnet.dj,abdek.housssein@gmail.com,dt.bss.abdifatah@gmail.com,abokor.ahmed.kadar@outlook.com'
            mail_to = 'abokor.ahmed.kadar@outlook.com, abokor.ahmed.kadar.nour@gmail.com'
            mail_subject = 'MONITORING TOPUP REQUEST'

            mail_message_body = """\
            <html>
            <head></head>
            <body>
                <p>Bonjour/Bonsoir,<br><br>
                Veuillez trouver ci-joint les requêtes détectées comme erreurs au niveau de la plateforme TopUp :<br><br>
                %s<br>
                %s<br><br>
                Vous trouverez plus de détails <a href="%s">ici</a><br><br>
                Cordialement,<br><br>
                XANA SYSTEM
                </p>
            </body>
            </html>
            """ % (alert_queue,alert_queue_hist,link)

            ###################################################################

            message = MIMEMultipart('alternative')
            message['Subject'] = mail_subject
            message['From'] = mail_from
            message['To'] = mail_to
            
            message.attach(MIMEText(mail_message_body, 'html'))

            # Sent Email
            server = smtplib.SMTP('smtp-mail.outlook.com', 587)
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.sendmail("xana.system.v2@outlook.com",mail_to.split(","),msg=message.as_string())
            server.close()

        if found:

            message = "Error TopUp reports errors found"
            etat = "E"

        else:

            message = "TopUp does not report errors"
            etat = "S"

        Logs.objects.create(date_time=datetime_now,process=PROCESS_NUMBER,message_description=message,etat=etat)

    pass