import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import requests

from providers.pmml import Pmml

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('immofinance.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

spreadsheet = client.open('Devoir MREX')

# get the first sheet of the Spreadsheet
worksheet = spreadsheet.get_worksheet_by_id(277729321)

provider = Pmml()
provider.fetch_buildings("Drummondville")
provider.export_to_worksheet(worksheet)