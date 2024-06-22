import csv
from collections import defaultdict
from datetime import datetime
import re
def remove_empty_rows(rows):
    filtered_rows = [row for row in rows if any(cell.strip() for cell in row)]
    return filtered_rows

def replace_empty_with_null(rows):
    return [[cell.replace("'","''").replace('"','\'') if cell else "NULL" for cell in row ] for row in rows]

def replace_noise(rows):
    return [ [re.sub(r'\'INVOICES\"|"INVOICES"',"INVOICES",cell, flags=re.IGNORECASE) for cell in row] for row in rows]

def combine_duplicates_4_primary_keys(rows, header, *primary_keys):
    combined_rows = defaultdict(lambda : [""] *len(header))
    seen = set()
    for row in rows:
        key =  tuple(row[header.index(k)]  for k in primary_keys)
        row_tuple = tuple(row)
        if row_tuple in seen:
            continue
        seen.add(row_tuple)
        if key in combined_rows:
            for i, value in enumerate(row):
                if header[i] not in primary_keys:
                    if not value:
                        value = combined_rows[key][i]
        else:
            combined_rows[key] = row
    return list(combined_rows.values())


def remove_NA(rows):
    updated_rows = []
    for row in rows:
        updated_row = ['' if cell == '#N/A' or cell=='New' else cell for cell in row ]
        updated_rows.append(updated_row)
    return updated_rows

def adjust_date(parsed_date):
    if parsed_date.year >= 2000:
        adjusted_year = parsed_date.year - 100  # Adjust the year to the 1900s range
        parsed_date = parsed_date.replace(year=adjusted_year)
    return parsed_date

def convert_datetime(rows, header, datetime_cols_lst):
    #10/28/21 0:00
    for index, row in enumerate(rows):
        for col_name in datetime_cols_lst:
            col_idx = header.index(col_name)
            datetime_str = row[col_idx].strip()
            if not datetime_str:
                row[col_idx] = "NULL"
                continue
            formats_to_try = ['%m/%d/%y %H:%M']
            date_obj = None
            for fmt in formats_to_try:
                try:
                    date_obj = datetime.strptime(datetime_str, fmt)
                    date_obj = adjust_date(date_obj)
                    row[col_idx] = date_obj.strftime('%Y-%m-%d %H:%M')
                    break  # Exit loop if format is successfully parsed
                except ValueError:
                    pass  # Continue to next format if current one fails
            if date_obj is None:
                print(f"Error converting date for column '{col_name}': {datetime_str}")
        rows[index] = row
    return rows



def convert_date(rows, header, date_col_lst):
    #updated_rows = []
    for index, row in enumerate(rows):

        for col_name in date_col_lst:
            col_idx = header.index(col_name)
            date_str = row[col_idx].strip()
            if not date_str:
                row[col_idx] = "NULL"
                continue
            if date_str:
                formats_to_try = ['%d/%m/%Y', '%d/%m/%y','%m/%d/%y']  # Add more formats as needed
                date_obj = None
                for fmt in formats_to_try:
                    try:
                        date_obj = datetime.strptime(date_str, fmt)
                        date_obj = adjust_date(date_obj)
                        row[col_idx] = date_obj.strftime('%Y-%m-%d')
                        break  # Exit loop if format is successfully parsed
                    except ValueError:
                        pass  # Continue to next format if current one fails
                if date_obj is None:
                    print(f"Error converting date for column '{col_name}': {date_str}")

        rows[index] = row
       #updated_rows.append(row)

    return rows
