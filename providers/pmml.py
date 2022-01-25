
import json
from gspread import Worksheet
from gspread.utils import ValueInputOption, ValueRenderOption, rowcol_to_a1
import random
import time
from typing import Dict
import requests
from bs4 import BeautifulSoup
from data_structures.pmml import PmmlDataStructure

from providers.provider import Provider

class Pmml(Provider):

    def __init__(self) -> None:
        self.buildings = []
        self.buildingLinks = []
        super().__init__()
    
    def fetch_buildings(self, city):
        '''
        To get all the buildings, use % symbol in query.
        buildingReq = requests.get("https://goplex.com/api/proprietes/avendre?q=%")
        '''
        req = requests.get("https://goplex.com/api/proprietes/avendre?q={}".format(city))
        for jsonBuilding in req.json():
            if jsonBuilding.get('sNomVille') == city:
                self.buildingLinks.append(dict({
                    "address": "%s %s" % (jsonBuilding.get('sNumeroCivique'), jsonBuilding.get('sRue')),
                    "link": jsonBuilding.get('sLien'),
                    "city": jsonBuilding.get('sNomVille'),
                }))
    
    def export_to_worksheet(self, worksheet: Worksheet):
        col = 3 # initial col

        worksheet.update_cell(24, 1, 195)
        worksheet.update_cell(25, 1, 0.03)
        worksheet.update_cell(26, 1, 550)
        worksheet.update_cell(27, 1, 0.05)
        worksheet.update_cell(29, 1, 0.03)
        worksheet.update_cell(33, 1, 0.49)
        worksheet.update_cell(36, 1, 0.02)

        for building in self.buildingLinks:
            link = "https://goplex.com/api/proprietes/avendre/{}".format(building.get('link'))
            buildingReq = requests.get(link)
            jsonData = buildingReq.json()

            print(link, buildingReq.status_code)

            structure = PmmlDataStructure(jsonData)

            worksheet.insert_cols([[
                structure.get_address(),
                structure.get_url(),
                structure.get_city(),
                structure.get_price(),
                structure.get_downpayment(col),
                structure.get_units_count(),
                structure.get_unit_types(),
                structure.get_price_per_unit(col),
                structure.get_potential_gross_income(),
                structure.get_avg_monthly_rent(col),
                structure.get_rents_price_diff_in_sector(col),
                structure.get_normalized_net_revenues(col),
                structure.get_tga(col),
                "225000",
                structure.get_delta_per_unit(col),
                structure.get_delta_new_construction(col),
                structure.get_renovation_price(col),
                structure.get_profit_per_unit(col),
                structure.get_value_creation(col),
                structure.get_municipal_taxes(),
                structure.get_school_taxes(),
                structure.get_insurances_price(),
                structure.get_energy_price(),
                structure.get_janitor_expenses(col),
                structure.get_vacancy(col),
                structure.get_annual_maintenance(col),
                structure.get_annual_management(col),
                structure.get_normalized_expenses(col),
                structure.get_annual_mortgage(col),
                structure.get_total_expenses(col),
                structure.get_expenses_percentage(col),
                structure.get_cashflow_before_taxes(col),
                structure.get_capitalisation_before_taxes(col),
                structure.get_total_non_speculative(col),
                structure.get_bi_factor_return(col),
                structure.get_hypothetical_appreciation(col),
                structure.get_tri_factor_return(col),
            ]], col, ValueInputOption.user_entered)

            col += 1

            # Simulate time between queries for more realism.
            time.sleep(random.randint(3, 7))