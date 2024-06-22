import os

from enum import Enum
folder = "Z://AgedCare"
folder4mysql = "Z://AgedCareMysql"
#folder4datatype = "datatype"
folder_4_data_sample = "data_sample"
folder_4_data_ori = "ori_sample"
folder_4_create_table = "create_table"
folder_4_insert_into_table = "insert_into_table"

folder4mysqlcleaned = os.path.join(folder4mysql,'cleaned')
template_file = os.path.join(folder,'excels', 'Import_Template_v0.0.29_updated (with Sample).xlsx')

folder_4_mysql_results = os.path.join(folder4mysql,'mysql_results')

class TemplateSheet(Enum):
    ClientNoteTypes = 'ClientNoteTypes'
    Groups = 'Groups'
    Contacts = 'Contacts'
    Clients = 'Clients'
    ClientContacts = 'ClientContacts'
    ClientGroups = 'ClientGroups'
    ClientNotes = 'ClientNotes'
    Services = 'Services'
    ServiceIdFunderCode = 'ServiceIdFunderCode'
    ServiceBillCodes = 'ServiceBillCodes'
    ServiceActivityCodes = 'ServiceActivityCodes'
    Visits = 'Visits'
    Recurrences = 'Recurrences'
    RecurrenceActivityCodes = 'RecurrenceActivityCodes'




