# run main.py to generate comm2.py

# clean data to get files in cleaned folder + data_sample
import helper
helper.create_enum_4_comm2()
import mysql_helper
import os
import comm
import clean
import comm2


for item in comm2.CSVFiles:
    fname = item.value
    headerStrategy, rowsStrategy = clean.select_strategy(fname)
    pipeline = clean.DataCleaningPipeline(rowsStrategy,headerStrategy, 'ContactId','ClientId')
    pipeline.execute_pipeline(fname)

for file in os.listdir(comm.folder_4_data_sample):
    table_name = mysql_helper.table_name_dict.get(file)
    mysql_helper.create_table(os.path.join(comm.folder_4_data_sample, file),
                              table_name)

mysql_helper.create_mysql_files_to_insert(comm.folder4mysqlcleaned)
