import re
import os
import json

import comm


def sql_table_col_names(folder):
    target_columns = []
    for file in os.listdir(folder):
        with open(os.path.join(folder, file)) as f:
            for line in f.readlines():
                if re.search('Yes|yes', line):
                    target_columns.append(re.sub(r'\*|\s|\n|yes|_|\?', '', line, flags=re.IGNORECASE).lower())

    return target_columns




folder = 'rst_cols'
target = sql_table_col_names(folder)
print('target is ',target)
pattern = r'\b\w*(?:' + '|'.join(map(re.escape, target)) + r')\w*\b'
print('pattern',pattern)
def updated_header(header):
    match_indices = []
    for index, h in enumerate(header):

        if re.search(pattern, h.replace('_',''), re.IGNORECASE):
            match_indices.append(index)
    header_updated = list(map(lambda i: header[i], match_indices))
    return header_updated, match_indices
#header = ['Check1', 'Id', 'Supplier_Name', 'Client_Type', 'Salutation', 'Full_Name', 'FirstName', 'LastName', 'Middle_Name', 'Preferred_Name', 'OtherPhoneNumber', 'EmailAddress', 'Schedule_Reminders', 'DateOfBirth', 'Gender', 'Address', 'City', 'PostalCode', 'Province', 'MainPhoneNumber', 'File_Under', 'Subscribe_to_Marketing', 'Country', 'Preferred_Service', 'Pack_Service', 'Status', 'IsClientCoordinatorNote', 'Content', 'Client_Alert_Notes', 'Billing_Client', 'Extra_Invoice_Info', 'Discount', 'How_did_you_hear_of_Healthlink', 'Created', 'Roles', 'IsArchived']

#print(updated_header(header))




# for file in [comm.CSVFiles.CLIENTS_DIT]:
#     with open(os.path.join(dest_folder,file)) as f:
#         content = json.load(f)
#     content = ' '.join(content)
#     rst = re.findall(pattern, content,re.IGNORECASE)
#     if rst:
#          print(f'{file} match {rst}')
#
