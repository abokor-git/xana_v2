from datetime import datetime
import json
from telnetlib import STATUS
from django_extensions.management.jobs import MinutelyJob

from iteration_utilities import duplicates
from iteration_utilities import unique_everseen

import cx_Oracle
from numpy import corrcoef
import psycopg2

import requests

from apps.app.models import DataPPBU

import pandas as pd

class Job(MinutelyJob):
    help = "My sample job."

    def execute(self):

        """ La date et l'heure """
        datetime_today = datetime.now()
        date_recharge_start = datetime_today.strftime("%Y-%m-01 00:00:00")
        date_recharge_end = datetime_today.strftime("%Y-%m-01 03:00:00")
        date_recharge_start = "2022-01-01 00:00:00"
        date_recharge_end = "2022-01-01 03:00:00"
        
        """ ORACLE """

        connection = cx_Oracle.connect(
            user="SYSADM",
            password="SYSADM",
            dsn="10.11.22.12/BSCSPROD.DJIBOUTITELECOM.DJ")

        cursor = connection.cursor()

        ID = []
        CO_CODE = []
        CO_ID = []
        TM_CODE = []
        DEBIT = []
        RECHARGE_CODE = []
        ENTRY_DATE = []
        PROCESSED_DATE = []
        STATUS = []
        RETRY = []
        MSISDN = []
        ERROR = []

        # Now query the rows back
        for row in cursor.execute("select * from BSSAPI.AUTO_RECHARGE_HIST where processed_date >= to_date('"+date_recharge_start+"', 'YYYY-MM-DD HH24:MI:SS') and processed_date <= to_date('"+date_recharge_end+"', 'YYYY-MM-DD HH24:MI:SS') and debit in ('A','AI','B','BI','C','CI','D','DI','E','EI','EX DG','EX DGI','F','FI','G','GI','H','HI','I','X')"):

            ID.append(row[0])
            CO_CODE.append(row[1])
            CO_ID.append(row[2])
            TM_CODE.append(row[3])
            DEBIT.append(row[4])
            RECHARGE_CODE.append(row[5])
            ENTRY_DATE.append(row[6])
            PROCESSED_DATE.append(row[7])
            STATUS.append(row[8])
            RETRY.append(row[9])
            MSISDN.append(row[10])
            ERROR.append(row[11])

        connection.commit()

        data = {
            'ID': ID,
            'CO_CODE': CO_CODE,
            'CO_ID': CO_ID,
            'TM_CODE': TM_CODE,
            'DEBIT': DEBIT,
            'RECHARGE_CODE': RECHARGE_CODE,
            'ENTRY_DATE': ENTRY_DATE,
            'PROCESSED_DATE': PROCESSED_DATE,
            'STATUS': STATUS,
            'RETRY': RETRY,
            'MSISDN': MSISDN,
            'ERROR': ERROR
        }

        cx = pd.DataFrame(data)

        ###################################################

        """ TOPUP """

        command_content = []
        updated_date = []
        error_description = []

        conn = psycopg2.connect(
            host="172.32.1.45",
            database="xana_db",
            user="postgres",
            password="postgrespwd",
            port="5432"
        )

        #Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        #Executing an MYSQL function using the execute() method
        cursor.execute("SELECT command_content, updated_date, error_description FROM app_queuehist where action_type=55 and created_date >= '"+date_recharge_start+"' and created_date <= '"+date_recharge_end+"' order by created_date;")

        # Fetch a single row using fetchone() method.
        data = cursor.fetchall()
        for row in data:
            command_content.append(row[0])
            updated_date.append(row[1])
            error_description.append(row[2])

        data = {
            'command_content': command_content,
            'updated_date': updated_date,
            'error_description': error_description
        }

        topup = pd.DataFrame(data)

        ############################################################

        quota = {
            'A': '5000.0',
            'AI': '5000.0',
            'B': '10000.0',
            'BI': '10000.0',
            'C': '15000.0',
            'CI': '15000.0',
            'D': '20000.0',
            'DI': '20000.0',
            'E': '30000.0',
            'EI': '30000.0',
            'EX DG': '70000.0',
            'EX DGI': '70000.0',
            'F': '50000.0',
            'FI': '50000.0',
            'G': '60000.0',
            'GI': '60000.0',
            'H': '100000.0',
            'HI': '100000.0',
            'I': 'AUTO_RECHARGE_I',
            'X': 'AUTO_RECHARGE_I'
        }

        list_id = []
        list_co_code = []
        list_co_id = []
        list_tm_code = []
        list_debit = []
        list_recharge_code = []
        list_entry_date = []
        list_processed_date = []
        list_status = []
        list_retry = []
        list_msisdn = list (cx['MSISDN'][ (cx['DEBIT'] != 'X') & (cx['DEBIT'] != 'I')])
        list_error = []
        list_command_content = []
        list_updated_date = []
        list_error_description = []

        for x in list_msisdn:
            
            num = str(x)
            index = MSISDN.index(x)
            list_id.append(ID[index])
            list_co_code.append(CO_CODE[index])
            list_co_id.append(CO_ID[index])
            list_tm_code.append(TM_CODE[index])
            list_debit.append(DEBIT[index])
            list_recharge_code.append(RECHARGE_CODE[index])
            list_entry_date.append(ENTRY_DATE[index])
            list_processed_date.append(PROCESSED_DATE[index])
            list_status.append(STATUS[index])
            list_retry.append(RETRY[index])
            list_error.append(ERROR[index])
            forfait = RECHARGE_CODE[index]
            cc = num+"#"+forfait
            
            if cc in command_content:

                id = command_content.index(cc)
                list_command_content.append(command_content[id])
                list_updated_date.append(updated_date[id])
                list_error_description.append(error_description[id])
            else:
                list_command_content.append('None')
                list_updated_date.append('None')
                list_error_description.append('None')

        #####################################################################

        list_type = []
        list_old_value = []
        list_new_value = []
        list_credited_amount = []
        list_old_exp = []
        list_new_exp = []
        list_profile = []

        for x in range(len(list_msisdn)):

            trouver = False

            date_topup = list_updated_date[x]

            if date_topup!='None':

                date_topup_timestamp = datetime.timestamp(date_topup)
                date_topup_timestamp_min = date_topup_timestamp-300
                date_topup_timestamp_max = date_topup_timestamp+300
                date_topup_min = datetime.fromtimestamp(date_topup_timestamp_min)
                date_topup_max = datetime.fromtimestamp(date_topup_timestamp_max)

                item = DataPPBU.objects.filter(date_recharge__range=[date_topup_min,date_topup_max],numero=list_msisdn[x])

                for y in item:
                    
                    cdr_detail = list(y.data.split(" "))

                    if 'XML' in cdr_detail:
                        index_xml = cdr_detail.index('XML')
                        if 'UPDATE_BALANCE' in cdr_detail:
                            index_update_balance = cdr_detail.index('UPDATE_BALANCE')
                            if index_xml<index_update_balance and 'COMMON' in cdr_detail[index_update_balance:]:
                                index_common = cdr_detail[index_update_balance:].index('COMMON')
                                nb = index_common+index_update_balance+1
                                cdr_quota = cdr_detail[nb]+'.0'

                                if cdr_quota==quota[list_debit[x]]:
                                    trouver=True
                                    list_type.append(cdr_detail[nb-1])
                                    list_old_value.append(cdr_detail[nb+3])
                                    list_new_value.append(cdr_detail[nb+2])
                                    list_credited_amount.append(cdr_quota)
                                    
                                    oldexp_year = cdr_detail[nb+4][0:4]
                                    oldexp_month = cdr_detail[nb+4][4:6]
                                    oldexp_day = cdr_detail[nb+4][6:8]
                                    oldexp_hour = cdr_detail[nb+4][8:10]
                                    oldexp_min = cdr_detail[nb+4][10:12]
                                    oldexp_sec = cdr_detail[nb+4][12:14]
                                    oldexp_date = oldexp_year+"-"+oldexp_month+"-"+oldexp_day+" "+oldexp_hour+":"+oldexp_min+":"+oldexp_sec
                                    
                                    newexp_year = cdr_detail[nb+5][0:4]
                                    newexp_month = cdr_detail[nb+5][4:6]
                                    newexp_day = cdr_detail[nb+5][6:8]
                                    newexp_hour = cdr_detail[nb+5][8:10]
                                    newexp_min = cdr_detail[nb+5][10:12]
                                    newexp_sec = cdr_detail[nb+5][12:14]
                                    newexp_date = newexp_year+"-"+newexp_month+"-"+newexp_day+" "+newexp_hour+":"+newexp_min+":"+newexp_sec
                                    
                                    list_old_exp.append(oldexp_date)
                                    list_new_exp.append(newexp_date)
                                    list_profile.append(y.profil_ocs)

                                    break

            if trouver==False:
                list_type.append('None')
                list_old_value.append('None')
                list_new_value.append('None')
                list_credited_amount.append('None')
                list_old_exp.append('None')
                list_new_exp.append('None')
                list_profile.append('None')

        #####################################################################

        data = {
            'ID': list_id,
            'CO_CODE': list_co_code,
            'CO_ID': list_co_id,
            'TM_CODE': list_tm_code,
            'DEBIT': list_debit,
            'RECHARGE_CODE': list_recharge_code,
            'ENTRY_DATE': list_entry_date,
            'PROCESSED_DATE': list_processed_date,
            'STATUS': list_status,
            'RETRY': list_retry,
            'MSISDN': list_msisdn,
            'ERROR': list_error,
            'COMMAND_CONTENT': list_command_content,
            'UPDATED_DATE': list_updated_date,
            'MESSAGE_DESCRIPTION': list_error_description,
            'TYPE': list_type,
            'OLD_VALUE': list_old_value,
            'NEW_VALUE': list_new_value,
            'CREDITED_AMOUNT': list_credited_amount,
            'OLD_EXP_DATE': list_old_exp,
            'NEW_EXP_DATE': list_new_exp,
            'PROFIL_OCS': list_profile
        }

        cx_topup = pd.DataFrame(data)
        cx_topup.to_csv('extraction.csv')
