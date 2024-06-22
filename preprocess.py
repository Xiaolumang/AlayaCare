import os
import csv
from collections import defaultdict
import json
import re
import comm


from abc import ABC, abstractmethod

class HeaderStrategy(ABC):
    @abstractmethod
    def clean(self, header):
        header = [col.replace(' ', '_')
                .replace('#', '')
                .replace('\n', '')
                .replace('*', '').replace('.', '')
                .replace('?', '')
                 for col in header]
        header = replace_4_duplicate_col_names(header, 'GroupName', 'Div', 'Type', 'Check')

        return header

def replace_4_duplicate_col_names(header, *args):
    for arg in args:
        count = 1
        for index, item in enumerate(header):
            if item == arg:
                header[index] =f'{item}{count}'
                count += 1
    return header
class SamisChspClientsDITHeaderStrategy(HeaderStrategy):
    def clean(self, header):
        header = super().clean(header)
        cols = [col.replace('<18','less_than_18').replace('18+','more_than_18')
                .replace('AS','AS1').replace('Postcode','PostalCode') for col in header]


        return cols
#
class DefaultHeaderStrategy(HeaderStrategy):
    def clean(self, header):
        header = super().clean(header)
        return header

#Services_DIT_UAT_bill_codes.csv
class Services_DIT_UAT_BillCodesStrategy(HeaderStrategy):
    def clean(self, header):
        header = super().clean(header)
        cols = [re.sub(r'\(.+\)','',col) for col in header ]
        return cols
# class HeaderProcessor:
#     def __init__(self, strategy: HeaderStrategy):
#         self.strategy = strategy
#
#     def process(self, header):
#         return self.strategy.process_header(header)



# def replace_csv_header(input_file, output_file, header):
#     with open(input_file, encoding='utf-8-sig') as infile:
#         csvreader = csv.reader(infile)
#         rows = list(csvreader)
#         rows[0] = header
#     with open(output_file,'w',newline='', encoding='utf-8-sig') as outfile:
#         csvwriter = csv.writer(outfile)
#         csvwriter.writerows(rows)
#
# def modified_columns(folder, file):
#     with open(os.path.join(folder, file), encoding='utf-8-sig') as csvfile:
#         csvreader = csv.reader(csvfile)
#         header = next(csvreader)
#         #print(header)
#         cols = [col.replace(' ', '_')
#                 .replace('#','')
#                 .replace('\n', '')
#                 .replace('*', '').replace('.','')
#                 .replace('Check', 'Check1').replace('?', '')
#                 .replace('Type','Type1') for col in header]
#
#         strategy = select_strategy(file)
#         processer = HeaderProcessor(strategy)
#         cols = processer.process(cols)
#     return cols

# def change_csv_header(folder, file):
#     cols = modified_columns(folder,file)
#     replace_csv_header(os.path.join(folder,file),os.path.join(comm.folder4mysql,file),cols)
#
# for file in comm.file_lst:
#     change_csv_header(comm.folder,file)

