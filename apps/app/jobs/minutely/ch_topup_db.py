from django_extensions.management.jobs import MinutelyJob

from datetime import datetime, timedelta

from apps.app.models import Logs
from apps.app.models import Queue, QueueHist
from apps.app.models import AlertQueue, AlertQueueHist

class Job(MinutelyJob):
    help = "Check TopUp data every 5 minutes"

    def execute(self):
        
        PROCESS_NUMBER = 1613

        """ La date et l'heure """
        time_in = "00:00:00"
        time_su = "23:59:59"
        datetime_today = datetime.now()
        datetime_yesterday = datetime.now()-timedelta(7)
        date_today = datetime_today.strftime("%Y-%m-%d")
        date_yesterday = datetime_yesterday.strftime("%Y-%m-%d")
        datetime_now = datetime_today.strftime("%Y-%m-%d %H:%M:%S")
        datetime_min = date_yesterday+" "+time_in
        datetime_max = date_today+" "+time_su

        tab_queue = Queue.objects.filter(created_date__range=[datetime_min,datetime_max])
        tab_queuehist = QueueHist.objects.filter(created_date__range=[datetime_min,datetime_max])

        for x in tab_queue:

            ERROR_ACTION_TYPE = False
            if x.action_type not in [1, 2, 3, 4, 5, 44, 55]:
                ERROR_ACTION_TYPE = True

            ERROR_COMMAND_CONTENT = False
            if x.command_content == None or x.command_content == "":
                ERROR_COMMAND_CONTENT = True

            ERROR_STATUS = False
            if x.status != 0:
                ERROR_STATUS = True

            ERROR_MSISDN = False
            if not (x.msisdn == "00000000" or (len(x.msisdn)==11 and x.msisdn[0:5] == "25377")) :
                ERROR_MSISDN = True
            
            ERROR_PINCODE = False
            if x.pincode == None:
                ERROR_PINCODE = True

            ERROR_ERROR_CODE = False
            if x.error_code not in [0, 3, 4, 5, 6, 16211, 16275, 16296, 100008, 100009, 100010, 100011]:
                ERROR_ERROR_CODE = True

            ERROR_ERROR_DESCRIPTION = False
            if x.error_description == None:
                ERROR_ERROR_DESCRIPTION = True

            ERROR_ETAT = False
            if x.etat != "E":
                ERROR_ETAT = True

            ERROR_THREAD_NAME = False
            if x.thread_name not in ["Thread 0", "Thread 1", "Thread 2", "Thread 3", "Thread 4"]:
                ERROR_THREAD_NAME = True

            ERROR_THREAD_NUMBER = False
            if x.thread_number not in [0, 5]:
                ERROR_THREAD_NUMBER = True

            ERROR_FEE = False
            if x.fee != 0:
                ERROR_FEE = True

            ERROR_IP_ADRESSE_CLIENT = False
            if x.ip_adresse_client not in ["10.11.22.8", "10.11.24.150", "10.11.24.151"]:
                ERROR_IP_ADRESSE_CLIENT = True

            ERROR_USERNAME = False
            if x.username not in ["topup", "USSDUSR"]:
                ERROR_USERNAME = True

            if ERROR_ACTION_TYPE or ERROR_COMMAND_CONTENT or ERROR_STATUS or ERROR_MSISDN or ERROR_PINCODE or ERROR_ERROR_CODE or ERROR_ERROR_DESCRIPTION or ERROR_ETAT or ERROR_THREAD_NAME or ERROR_THREAD_NUMBER or ERROR_FEE or ERROR_IP_ADRESSE_CLIENT or ERROR_USERNAME:

                itemExistOnAlertQueue = AlertQueue.objects.filter(id_queue=x.id).exists()

                if not itemExistOnAlertQueue:

                    ItemQueue = Queue.objects.get(id_queue=x.id_queue)
                    AlertQueue.objects.create(check_1=False,check_2=False,check_3=False,reported=False,corrected=False,id_queue=ItemQueue)
            
        for y in tab_queuehist:

            ERROR_ACTION_TYPE = False
            if y.action_type not in [1, 2, 3, 4, 5, 44, 55]:
                ERROR_ACTION_TYPE = True

            ERROR_COMMAND_CONTENT = False
            if y.command_content == None or y.command_content == "":
                ERROR_COMMAND_CONTENT = True

            ERROR_STATUS = False
            if y.status not in [0, 1]:
                ERROR_STATUS = True

            ERROR_ERROR_DESCRIPTION = False
            if y.error_description != "Opération effectué avec success !!!":
                ERROR_ERROR_DESCRIPTION = True

            ERROR_MSISDN = False
            if not (y.msisdn == "00000000" or (len(y.msisdn)==11 and y.msisdn[0:5] == "25377")) :
                ERROR_MSISDN = True

            ERROR_PINCODE = False
            if y.pincode == None:
                ERROR_PINCODE = True

            ERROR_ETAT = False
            if y.etat != "S":
                ERROR_ETAT = True

            ERROR_THREAD_NAME = False
            if y.thread_name not in ["Thread 0", "Thread 1", "Thread 2", "Thread 3", "Thread 4"]:
                ERROR_THREAD_NAME = True

            ERROR_THREAD_NUMBER = False
            if y.thread_number not in [0, 5]:
                ERROR_THREAD_NUMBER = True

            ERROR_FEE = False
            if y.fee == None:
                ERROR_FEE = True

            ERROR_IP_ADRESSE_CLIENT = False
            if y.ip_adresse_client not in ["10.11.22.8", "10.11.24.150", "10.11.24.151"]:
                ERROR_IP_ADRESSE_CLIENT = True

            ERROR_USERNAME = False
            if y.username not in ["topup", "USSDUSR"]:
                ERROR_USERNAME = True

            if ERROR_ACTION_TYPE or ERROR_COMMAND_CONTENT or ERROR_STATUS or ERROR_MSISDN or ERROR_PINCODE or ERROR_ERROR_CODE or ERROR_ERROR_DESCRIPTION or ERROR_ETAT or ERROR_THREAD_NAME or ERROR_THREAD_NUMBER or ERROR_FEE or ERROR_IP_ADRESSE_CLIENT or ERROR_USERNAME:

                itemExistOnAlertQueueHist = AlertQueueHist.objects.filter(id_queue_hist=y.id).exists()

                if not itemExistOnAlertQueueHist:

                    ItemQueueHist = QueueHist.objects.get(id_queue_hist=y.id_queue_hist)
                    AlertQueueHist.objects.create(check_1=False,check_2=False,check_3=False,reported=False,corrected=False,id_queue_hist=ItemQueueHist)

        item_check_queue = AlertQueue.objects.filter(reported=False)
        
        for x in item_check_queue:

            item_queue = x.id_queue

            ERROR_ACTION_TYPE = False
            if item_queue.action_type not in [1, 2, 3, 4, 5, 44, 55]:
                ERROR_ACTION_TYPE = True

            ERROR_COMMAND_CONTENT = False
            if item_queue.command_content == None or item_queue.command_content == "":
                ERROR_COMMAND_CONTENT = True

            ERROR_STATUS = False
            if item_queue.status != 0:
                ERROR_STATUS = True

            ERROR_MSISDN = False
            if not (item_queue.msisdn == "00000000" or (len(item_queue.msisdn)==11 and item_queue.msisdn[0:5] == "25377")) :
                ERROR_MSISDN = True
            
            ERROR_PINCODE = False
            if item_queue.pincode == None:
                ERROR_PINCODE = True

            ERROR_ERROR_CODE = False
            if item_queue.error_code not in [0, 3, 4, 5, 6, 16211, 16275, 16296, 100008, 100009, 100010, 100011]:
                ERROR_ERROR_CODE = True

            ERROR_ERROR_DESCRIPTION = False
            if item_queue.error_description == None:
                ERROR_ERROR_DESCRIPTION = True

            ERROR_ETAT = False
            if item_queue.etat != "E":
                ERROR_ETAT = True

            ERROR_THREAD_NAME = False
            if item_queue.thread_name not in ["Thread 0", "Thread 1", "Thread 2", "Thread 3", "Thread 4"]:
                ERROR_THREAD_NAME = True

            ERROR_THREAD_NUMBER = False
            if item_queue.thread_number not in [0, 5]:
                ERROR_THREAD_NUMBER = True

            ERROR_FEE = False
            if item_queue.fee != 0:
                ERROR_FEE = True

            ERROR_IP_ADRESSE_CLIENT = False
            if item_queue.ip_adresse_client not in ["10.11.22.8", "10.11.24.150", "10.11.24.151"]:
                ERROR_IP_ADRESSE_CLIENT = True

            ERROR_USERNAME = False
            if item_queue.username not in ["topup", "USSDUSR"]:
                ERROR_USERNAME = True

            if ERROR_ACTION_TYPE or ERROR_COMMAND_CONTENT or ERROR_STATUS or ERROR_MSISDN or ERROR_PINCODE or ERROR_ERROR_CODE or ERROR_ERROR_DESCRIPTION or ERROR_ETAT or ERROR_THREAD_NAME or ERROR_THREAD_NUMBER or ERROR_FEE or ERROR_IP_ADRESSE_CLIENT or ERROR_USERNAME:

                if x.check_1 == False:

                    AlertQueue.objects.filter(id=x.id).update(check_1=True)

                else:

                    if x.check_2 == False:

                        AlertQueue.objects.filter(id=x.id).update(check_2=True)

                    else:

                        AlertQueue.objects.filter(id=x.id).update(check_3=True)

            else:

                AlertQueue.objects.filter(id=x.id).delete()

        item_check_queue_hist = AlertQueueHist.objects.filter(reported=False)

        for y in item_check_queue_hist:

            item_queue_hist = y.id_queue_hist

            ERROR_ACTION_TYPE = False
            if item_queue_hist.action_type not in [1, 2, 3, 4, 5, 44, 55]:
                ERROR_ACTION_TYPE = True

            ERROR_COMMAND_CONTENT = False
            if item_queue_hist.command_content == None or item_queue_hist.command_content == "":
                ERROR_COMMAND_CONTENT = True

            ERROR_STATUS = False
            if item_queue_hist.status != 0:
                ERROR_STATUS = True

            ERROR_MSISDN = False
            if not (item_queue_hist.msisdn == "00000000" or (len(item_queue_hist.msisdn)==11 and item_queue_hist.msisdn[0:5] == "25377")) :
                ERROR_MSISDN = True
            
            ERROR_PINCODE = False
            if item_queue_hist.pincode == None:
                ERROR_PINCODE = True

            ERROR_ERROR_CODE = False
            if item_queue_hist.error_code not in [0, 3, 4, 5, 6, 16211, 16275, 16296, 100008, 100009, 100010, 100011]:
                ERROR_ERROR_CODE = True

            ERROR_ERROR_DESCRIPTION = False
            if item_queue_hist.error_description == None:
                ERROR_ERROR_DESCRIPTION = True

            ERROR_ETAT = False
            if item_queue_hist.etat != "E":
                ERROR_ETAT = True

            ERROR_THREAD_NAME = False
            if item_queue_hist.thread_name not in ["Thread 0", "Thread 1", "Thread 2", "Thread 3", "Thread 4"]:
                ERROR_THREAD_NAME = True

            ERROR_THREAD_NUMBER = False
            if item_queue_hist.thread_number not in [0, 5]:
                ERROR_THREAD_NUMBER = True

            ERROR_FEE = False
            if item_queue_hist.fee != 0:
                ERROR_FEE = True

            ERROR_IP_ADRESSE_CLIENT = False
            if item_queue_hist.ip_adresse_client not in ["10.11.22.8", "10.11.24.150", "10.11.24.151"]:
                ERROR_IP_ADRESSE_CLIENT = True

            ERROR_USERNAME = False
            if item_queue_hist.username not in ["topup", "USSDUSR"]:
                ERROR_USERNAME = True

            if ERROR_ACTION_TYPE or ERROR_COMMAND_CONTENT or ERROR_STATUS or ERROR_MSISDN or ERROR_PINCODE or ERROR_ERROR_CODE or ERROR_ERROR_DESCRIPTION or ERROR_ETAT or ERROR_THREAD_NAME or ERROR_THREAD_NUMBER or ERROR_FEE or ERROR_IP_ADRESSE_CLIENT or ERROR_USERNAME:

                if y.check_1 == False:

                    AlertQueueHist.objects.filter(id=y.id).update(check_1=True)

                else:

                    if y.check_2 == False:

                        AlertQueueHist.objects.filter(id=y.id).update(check_2=True)

                    else:

                        AlertQueueHist.objects.filter(id=y.id).update(check_3=True)

            else:

                AlertQueueHist.objects.filter(id=y.id).delete()
        
        message = "TopUp check data"
        etat = "S"
        Logs.objects.create(date_time=datetime_now,process=PROCESS_NUMBER,message_description=message,etat=etat)

    pass