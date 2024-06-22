import os
import re
from collections import defaultdict

import csv
from collections import defaultdict
from enum import Enum

import comm
import comm2

import re
rst = re.search(r'"Invoice"', '\"INVOICE\"',re.IGNORECASE)
print(rst)

xx = ["NULL",'tis']
print(','.join(xx))
exit(0)
def header_length(folder,fname):
    with open(os.path.join(folder, fname), encoding='utf-8-sig') as f:
        csvreader = csv.reader(f)
        return len(next(csvreader))

def compare_header_length(fname):
    return header_length(os.path.join(comm.folder4mysql), fname), header_length(os.path.join(comm.folder4mysqlcleaned),fname)


for fname in comm2.CSVFiles:
    print(compare_header_length(fname.value))

exit(0)


exit(0)
# class Color(Enum):
#     RED = 'a red car.csv'
#     GREEN = 2
# print(Color.RED.value)
print(os.path.basename(os.path.join(comm.folder4mysqlcleaned,'abc.xxx')))


exit(0)
dest = 'rst_cols'
with open(os.path.join(dest, 'Contacts'), 'r') as f:
    cols = []
    for line in f:
        if re.search('Yes', line):
            cols.append(re.sub('Yes', '',line).strip())
    print(',\n'.join(cols))


exit(0)
xx = [('this','is'),('a','test')]
if ('a','test') in xx:
    print('he0llo')
exit(0)

f1 = open(os.path.join(folder, fname1),'w')
with open(os.path.join(folder, fname), 'r',encoding='utf-8') as f:
    for x in f.readlines():
        line = x.lstrip('\ufeff').strip()
        if line:
            f1.write(line+'\n')
f1.close()
exit(0)
cleaned_col = []
parts = sql.split(',')
for part in parts:
    if part.strip():
        cleaned_part = part.strip().replace(" ","_").replace("\n","")
        cleaned_col.append(cleaned_part)

table_name = 'PowerDiary'
default_datatype = 'varchar(255)'
column_definition = ',\n'.join([f'{col} {default_datatype}' for col in cleaned_col])
create_table_query = f'create table if not exists {table_name} \n ({column_definition})'
print(create_table_query)


