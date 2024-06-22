import os

import comm
import comm2
import json
import os
from collections import defaultdict
import helper
import csv
import re

folder = 'data_sample'
data_type_mapping = {
    'Id':'INT',
    'ClientId':'INT',
    'ContactId':'INT',
    'DateOfBirth':'DATE',
    'SAMIS_ID':'INT',
    'Power_Diary_Client_ID':'INT',
    'dtInvoicePaid':'DATETIME',
    'ServiceId':'INT',
    'Rate':'INT'

}

def mysql_alias(path):
    with open(path,'r') as f:
        alias = []
        lines = f.readlines()
        for line in lines:
            line = re.sub('yes|Yes', '', line).strip()
            alias.append(line)
    print(alias)
mysql_alias(os.path.join('rst_cols','Clients'))
table_name_dict= {comm2.NoCSVFiles.CLIENTS_DIT.value:'clients_dit',
            comm2.NoCSVFiles.SAMIS_CHSP_Clients_DIT_RI.value:'samis_chsp_clients_dit_ri',
                  comm2.NoCSVFiles.CONTACTS_DIT_ClientContacts.value:'contacts_dit_client_contacts',
                  comm2.NoCSVFiles.CONTACTS_DIT_Third_Parties.value:'contacts_dit_third_parties',
                  comm2.NoCSVFiles.ClientContacts_DIT_Invoices.value:'client_contacts_dit_invoices',
                  comm2.NoCSVFiles.GROUPS_DIT.value:'groups_dit',
                  comm2.NoCSVFiles.Services_DIT_UAT_bill_codes.value:'services_dit_uat_bill_codes',
                  comm2.NoCSVFiles.SERVICES_DIT_Invoice_Items.value:'services_dit_invoice_items'}


def all_table_columns():
    columns = set()
    for file in os.listdir(folder):
        with open(os.path.join(folder, file),'r') as f:
            data = json.load(f)
            columns.update(data.keys())
    return columns

def get_data_type(col_lst):
    return [data_type_mapping.get(key, 'VARCHAR(255)') for key in col_lst]
def column_definition(header):
    dt = get_data_type(header)

    definition = ',\n'.join(f'{k} {v}' for k, v in zip(header, dt))
    return  definition

def create_table(path, table_name):
    dest_folder = 'create_table'
    with open(path,'r', encoding='utf-8-sig') as f:
        data = json.load(f)

    column_def = column_definition(data.keys())
    drop_table_query = f'drop table if exists {table_name};\n'
    create_table_query = f'create table if not exists {table_name}\n ({column_def});'
    query = drop_table_query+create_table_query
    with open(os.path.join(dest_folder, helper.base_filename(path)), 'w') as f:
        f.write(query)

def get_value_part(row, quote_indies):
    for i, item in enumerate(row):
        if i in quote_indies:
            row[i] = f'"{item}"'
    return f"({', '.join(row)})"
def get_indices_4_quotes(header):
    indices = []
    for i, item in enumerate(header):
        if item not in data_type_mapping or data_type_mapping.get(item) == 'DATE'\
                or data_type_mapping.get(item) == 'DATETIME':
            indices.append(i)
    return indices


def replace_quotes_4_null(fname):
    with open(fname, 'r') as f:
        content = f.read()
    content = re.sub(r'"NULL"', "NULL", content)
    with open(fname, 'w') as f:
        f.write(content)
def insert_into_table(table_name, header, rows, fname):
    columns_part = f'{", ".join(header)}'
    values_part = ',\n'.join(map(lambda x: get_value_part(x,get_indices_4_quotes(header)), rows))
    insert_definition = f'insert into {table_name} ({columns_part}) values \n{values_part};'
    path = os.path.join(comm.folder_4_insert_into_table, fname)
    with open( path, 'w') as f:
        f.write(insert_definition)
    replace_quotes_4_null(path)


def get_csv_info(path):
    with open(path,'r') as f:
        csvreader = csv.reader(f)
        header = next(csvreader)
        rows = list(csvreader)
    return header, rows

def create_mysql_files_to_insert(source):
    for file in os.listdir(source):
        if file.endswith('csv'):
            header, rows = get_csv_info(os.path.join(source,file))
            fname = helper.base_filename(file)
            table_name = table_name_dict.get(fname)
            insert_into_table(table_name,header, rows, fname)

def select_column_names(fname):
    dest = 'rst_cols'
    cols = []
    with open(os.path.join(dest, fname)) as f:
        lines = f.readlines()
        for line in lines:
            if re.search('Yes|yes', line, flags=re.IGNORECASE):
                cols.append(re.sub(r'Yes|yes', '', line, flags=re.IGNORECASE).strip())
            else:
                cols.append('NULL as '+line.strip())
    rst = ',\n'.join(cols)
    print(rst)

select_column_names('Services')



