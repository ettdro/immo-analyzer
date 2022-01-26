from gspread import Worksheet
import time
import requests
from data_structures.pmml import PmmlDataStructure

from providers.provider import Provider

class Pmml(Provider):

    def __init__(self, worksheet: Worksheet) -> None:
        self.buildingLinks = []
        self.baseURL = "https://goplex.com/api/proprietes/avendre"
        super().__init__(worksheet)
    
    def fetch_buildings(self, city):
        '''
        To get all the buildings, use % symbol in query.
        buildingReq = requests.get("https://goplex.com/api/proprietes/avendre?q=%")
        '''
        req = requests.get(self.baseURL + "?q={}".format(city))
        for jsonBuilding in req.json():
            if jsonBuilding.get('sNomVille') == city:
                self.buildingLinks.append(dict({
                    "address": "%s %s" % (jsonBuilding.get('sNumeroCivique'), jsonBuilding.get('sRue')),
                    "link": jsonBuilding.get('sLien'),
                    "city": jsonBuilding.get('sNomVille'),
                }))
    
    def export_to_worksheet(self):
        for building in self.buildingLinks:
            link = self.baseURL + "/{}".format(building.get('link'))
            buildingReq = requests.get(link)
            jsonData = buildingReq.json()

            print(link, buildingReq.status_code)

            super().export_to_worksheet(PmmlDataStructure(jsonData, super().get_next_empty_row()))

            # Simulate time between queries for more realism.
            time.sleep(1)