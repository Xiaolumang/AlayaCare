import os
import comm
import csv
import comm2
from collections import defaultdict
from datetime import datetime
import clean_helper
import preprocess
import helper
import remove_cols_helper


#######
from abc import ABC, abstractmethod

class RowCleanStrategy(ABC):
    @abstractmethod
    def clean(self,rows, header,*primary_keys):
        pass

class Groups_DITRowsCleanStrategy(RowCleanStrategy):
    def clean(self,rows, header,*primary_keys):
        rows = clean_helper.remove_empty_rows(rows)
        return rows

class ClientsDITRowsCleanStrategy(RowCleanStrategy):
    def clean(self,rows, header,*primary_keys):
        rows = clean_helper.remove_empty_rows(rows)
        rows = clean_helper.convert_date(rows, header, ['DateOfBirth'])

        return rows
class ClientContactsDITInvoicesRowsCleanStrategy(RowCleanStrategy):
    def clean(self,rows, header,*primary_keys):
        rows = clean_helper.convert_datetime(rows, header, ['dtInvoicePaid'])
        return rows
class DefaultRowsCleanStrategy(RowCleanStrategy):
    def clean(self,rows, header,*primary_keys):
        rows = clean_helper.remove_empty_rows(rows)
        return rows
class Samis_Chsp_Clients_DITRowsCleanStrategy(RowCleanStrategy):
    def clean(self,rows, header,*primary_keys):
        # rows = convert_date(rows, header, ['Case_Open_Date','DOB'])
        rows = clean_helper.remove_NA(rows)
        return rows
class Contacts_DIT_ClientContactsStrategy(RowCleanStrategy):
    def clean(self,rows, header, *primary_keys):
        rows = clean_helper.combine_duplicates_4_primary_keys(rows,header,*primary_keys)
        rows = clean_helper.remove_NA(rows)
        return rows
class Contacts_DIT_Third_Parties(RowCleanStrategy):
    def clean(self,rows, header,*primary_keys):
        rows = clean_helper.replace_noise(rows)
        return rows


def select_strategy(file):
    if file == comm2.CSVFiles.SAMIS_CHSP_Clients_DIT_RI.value:
        return preprocess.SamisChspClientsDITHeaderStrategy(), Samis_Chsp_Clients_DITRowsCleanStrategy()
    if file == "Services_DIT_UAT_bill_codes.csv":
        return preprocess.Services_DIT_UAT_BillCodesStrategy(), DefaultRowsCleanStrategy()
    elif file == comm2.CSVFiles.GROUPS_DIT.value:
        return preprocess.DefaultHeaderStrategy(), Groups_DITRowsCleanStrategy()
    elif file == comm2.CSVFiles.CLIENTS_DIT.value:
        return preprocess.DefaultHeaderStrategy(), ClientsDITRowsCleanStrategy()
    elif file == comm2.CSVFiles.CONTACTS_DIT_ClientContacts.value:
        return preprocess.DefaultHeaderStrategy(), Contacts_DIT_ClientContactsStrategy()
    elif file == comm2.CSVFiles.CONTACTS_DIT_Third_Parties.value:
        return preprocess.DefaultHeaderStrategy(), Contacts_DIT_Third_Parties()
    elif file == comm2.CSVFiles.ClientContacts_DIT_Invoices.value:
        return preprocess.DefaultHeaderStrategy(), ClientContactsDITInvoicesRowsCleanStrategy()
    else:
        return preprocess.DefaultHeaderStrategy(), DefaultRowsCleanStrategy()
class DataCleaningPipeline:
    def __init__(self, row_cleaning_strategy, header_cleaning_strategy, *primary_keys):
        self.row_cleaning_strategy = row_cleaning_strategy
        self.header_cleaning_strategy = header_cleaning_strategy
        self.input_folder = comm.folder4mysql
        self.output_folder = comm.folder4mysqlcleaned
        self.primary_keys = primary_keys

    def set_row_strategy(self, row_cleaning_strategy):
        self.row_cleaning_strategy = row_cleaning_strategy

    def set_header_strategy(self, header_cleaning_strategy):
        self.header_cleaning_strategy = header_cleaning_strategy

    def execute_pipeline(self, filename):
        print(f'cleaning {filename}')
        input_file = os.path.join(self.input_folder, filename)
        output_file = os.path.join(self.output_folder, filename)

        rows, header = self.read_csv_file(input_file)

        #clean header
        header = self.header_cleaning_strategy.clean(header)
        helper.header_mapping_helper(header, rows[0], filename.rsplit('.')[0], comm.folder_4_data_ori)
        #reduce columns
        header, keep = remove_cols_helper.updated_header(header)

        #clean rows
        rows = self.row_cleaning_strategy.clean([list(map(lambda i: row[i], keep)) for row in rows], header,*self.primary_keys)

        helper.header_mapping_helper(header,rows[0],filename.rsplit('.')[0], comm.folder_4_data_sample)
        self.save_csv_file(output_file, header, rows)


    def read_csv_file(self, input_file):
        with open(input_file, 'r', encoding='utf-8-sig') as infile:
            csvreader = csv.reader(infile)
            if os.path.basename(input_file) == comm2.CSVFiles.SAMIS_CHSP_Clients_DIT_RI.value:
                next(csvreader)
            header = next(csvreader)
            rows = list(csvreader)
        return rows, header

    def save_csv_file(self, output_file, header, rows):
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            csvwriter = csv.writer(outfile)
            rows = clean_helper.replace_empty_with_null(rows)
            csvwriter.writerow(header)
            csvwriter.writerows(rows)




