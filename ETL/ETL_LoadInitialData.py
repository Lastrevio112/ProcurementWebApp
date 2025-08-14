"""THIS SCRIPT CONNECTS TO DATABASE AND LOADS SOURCE DATA INTO A DATA FRAME."""

import pandas as pd

#Storing the source data path:
SourceData_PATH = r"D:\EVERYTHING_PROGRAMMING\ProcurementSpendProject\Python_Project\Data\SourceData_Expenses.xlsx"

#Reading each sheet of the Excel in the SourceData_PATH into a big pandas dataframe
def read_all_sheets_to_df(excel_path: str, include_sheet_name: bool = True) -> pd.DataFrame:
    # Read all sheets into a dict of DataFrames
    all_sheets = pd.read_excel(excel_path, sheet_name=None)

    # Optionally add a column for sheet name, then collect into a list
    df_list = []
    for sheet_name, df in all_sheets.items():
        # Checking to see if the sheet_name is in the format YYYYMM
        if include_sheet_name and sheet_name.isdigit() and len(sheet_name) == 6:
            df = df.copy()
            df['sheet_name'] = sheet_name
        df_list.append(df)

    # Concatenate all DataFrames into one
    combined_df = pd.concat(df_list, ignore_index=True)

    # To fix a bug where INTERNET transactions weren't processed as it was wrongly spelled with a blank space at the end
    combined_df = combined_df.rename(columns=lambda x: x.strip())

    return combined_df

def return_df():
    return read_all_sheets_to_df(SourceData_PATH)