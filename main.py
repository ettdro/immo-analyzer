import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

from providers.pmml import Pmml
from providers.remax import Remax

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('immofinance.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

spreadsheet = client.open('Devoir MREX')

# get the first sheet of the Spreadsheet
worksheet = spreadsheet.get_worksheet_by_id(277729321)

# Worksheet static cells initialization
worksheet.update_cell(1, 24, 195)
worksheet.update_cell(1, 25, 0.03)
worksheet.update_cell(1, 26, 550)
worksheet.update_cell(1, 27, 0.05)
worksheet.update_cell(1, 29, 0.03)
worksheet.update_cell(1, 33, 0.49)
worksheet.update_cell(1, 36, 0.02)
worksheet.update_cell(1, 38, 0.04)
worksheet.update_cell(1, 42, 0.05)
worksheet.update_cell(1, 52, 0.75)

providers = [
    Pmml(worksheet),
    Remax(worksheet)
]

cities = [
    "Drummondville",
    "Sherbrooke"
]

for provider in providers:
    for city in cities:
        provider.fetch_buildings(city)
        provider.export_to_worksheet()
        provider.after_export()