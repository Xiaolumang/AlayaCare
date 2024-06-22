from enum import Enum
class CSVFiles(Enum):
    SAMIS_CHSP_Clients_DIT_RI = 'SAMIS CHSP Clients_DIT_RI.csv'
    CONTACTS_DIT_ClientContacts = 'CONTACTS_DIT_ClientContacts.csv'
    GROUPS_DIT = 'GROUPS_DIT.csv'
    CONTACTS_DIT_Third_Parties = 'CONTACTS_DIT_Third Parties.csv'
    Services_DIT_UAT_bill_codes = 'Services_DIT_UAT_bill_codes.csv'
    CLIENTS_DIT = 'CLIENTS_DIT.csv'
    SERVICES_DIT_Invoice_Items = 'SERVICES_DIT_Invoice Items.csv'
    ClientContacts_DIT_Invoices = 'ClientContacts_DIT_Invoices.csv'

class NoCSVFiles(Enum):
    SAMIS_CHSP_Clients_DIT_RI = 'SAMIS CHSP Clients_DIT_RI'
    CONTACTS_DIT_ClientContacts = 'CONTACTS_DIT_ClientContacts'
    GROUPS_DIT = 'GROUPS_DIT'
    CONTACTS_DIT_Third_Parties = 'CONTACTS_DIT_Third Parties'
    Services_DIT_UAT_bill_codes = 'Services_DIT_UAT_bill_codes'
    CLIENTS_DIT = 'CLIENTS_DIT'
    SERVICES_DIT_Invoice_Items = 'SERVICES_DIT_Invoice Items'
    ClientContacts_DIT_Invoices = 'ClientContacts_DIT_Invoices'

class Sheets(Enum):
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

