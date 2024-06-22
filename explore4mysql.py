import os
from collections import defaultdict
import csv
import comm
#file = 'SAMIS CHSP Clients_DIT.csv'

def bad_rows_4_primary_key(cnt_dict):
    filtered = {key: value for key, value in cnt_dict.items() if value !=1}
    print(filtered)
    return filtered.keys()

def print_bad_rows(fname, cnt_dict, p_key_names):
    bad = bad_rows_4_primary_key(cnt_dict)
    if not bad:
        print(f'unique for {p_key_names}')
        return
    row = 2
    with open(os.path.join(comm.folder4mysqlcleaned,fname), encoding='utf-8-sig') as f:
        csvreader = csv.DictReader(f)
        for content in csvreader:
            if tuple(content[k] for k in p_key_names) in bad:
                print(f'row {row} {content} ')
            row += 1

def count_primary_key(filename, *args):

    folder = comm.folder4mysqlcleaned


    with open(os.path.join(folder, filename), encoding='utf-8-sig') as f:
        csvreader = csv.DictReader(f)
       # print(next(csvreader))
        my_dict = defaultdict(int)
        # print(args)
        for content in csvreader:
            p_value = tuple(content[arg] for arg in args)
            my_dict[p_value] += 1
    return my_dict


def check_4_primary_key(fname,*primary_key_names):
    print(f'checking for {fname}  {primary_key_names}')
    cnt_dict = count_primary_key(fname, *primary_key_names)
    print_bad_rows(fname, cnt_dict,primary_key_names)

#check_4_primary_key(comm.file_lst[1], False, "SAMIS_ID" )
#check_4_primary_key(comm.file_lst[4], "Id")  # Clients_DIT
#check_4_primary_key(comm.file_lst[0],'ClientId','ContactId')
#check_4_primary_key(comm.file_lst[2],'ContactId')
def get_dict_values(row_dict, keys):
    return tuple(row_dict[k] for k in keys)

def get_all_values(fname, col_lst):
    s = set()
    with open(os.path.join(comm.folder4mysqlcleaned, fname), encoding='utf-8-sig') as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            s.add(get_dict_values(row, col_lst))
    return s
def foreign_key_check(fname1, cols1_lst, fname2, cols2_lst):
    set1 = get_all_values(fname1, cols1_lst)
    set2 = get_all_values(fname2, cols2_lst)
    print(len(set1), len(set2))
    print(len(set1-set2), len(set2-set1))
    print(len(set2 & set1))
#foreign_key_check('Clients_DIT.csv',['Id'],'SAMIS CHSP Clients_DIT.csv',['Power_Diary'])
foreign_key_check(comm.file_lst[2],['ContactId'], comm.file_lst[0],['ContactId'])



# file_lst = ['Contacts_DIT_ClientContacts.csv',
#             'SAMIS CHSP Clients_DIT.csv',
#             'CONTACTS_DIT_Third Parties.csv',
#             'GROUPS_DIT.csv',
#             'Clients_DIT.csv',
#             'ClientContacts_DIT_Invoices.csv',
#             'Services_DIT_UAT_bill_codes.csv',
#             'SERVICES_DIT_Invoice Items.csv']
