
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
        row = 3 # initial row

        worksheet.update_cell(1, 24, 195)
        worksheet.update_cell(1, 25, 0.03)
        worksheet.update_cell(1, 26, 550)
        worksheet.update_cell(1, 27, 0.05)
        worksheet.update_cell(1, 29, 0.03)
        worksheet.update_cell(1, 33, 0.49)
        worksheet.update_cell(1, 36, 0.02)
        worksheet.update_cell(1, 38, 0.04)

        for building in self.buildingLinks:
            link = "https://goplex.com/api/proprietes/avendre/{}".format(building.get('link'))
            buildingReq = requests.get(link)
            jsonData = buildingReq.json()

            print(link, buildingReq.status_code)

            structure = PmmlDataStructure(jsonData, row)

            worksheet.insert_row([
                structure.get_address(),
                structure.get_url(),
                structure.get_city(),
                structure.get_price(),
                structure.get_downpayment(),
                structure.get_units_count(),
                structure.get_unit_types(),
                structure.get_price_per_unit(),
                structure.get_potential_gross_income(),
                structure.get_avg_monthly_rent(),
                structure.get_rents_price_diff_in_sector(),
                structure.get_normalized_net_revenues(),
                structure.get_tga(),
                "225000",
                structure.get_delta_per_unit(),
                structure.get_delta_new_construction(),
                structure.get_renovation_price(),
                structure.get_profit_per_unit(),
                structure.get_value_creation(),
                structure.get_municipal_taxes(),
                structure.get_school_taxes(),
                structure.get_insurances_price(),
                structure.get_energy_price(),
                structure.get_janitor_expenses(),
                structure.get_vacancy(),
                structure.get_annual_maintenance(),
                structure.get_annual_management(),
                structure.get_normalized_expenses(),
                structure.get_annual_mortgage(),
                structure.get_total_expenses(),
                structure.get_expenses_percentage(),
                structure.get_cashflow_before_taxes(),
                structure.get_capitalisation_before_taxes(),
                structure.get_total_non_speculative(),
                structure.get_bi_factor_return(),
                structure.get_hypothetical_appreciation(),
                structure.get_tri_factor_return(),
                structure.get_joint_tga(),
                structure.get_jvm(),
                structure.get_deal_or_no_deal()
            ], row, ValueInputOption.user_entered)

            row += 1

            # Simulate time between queries for more realism.
            time.sleep(random.randint(3, 7))