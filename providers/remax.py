import time
import re
from bs4 import BeautifulSoup
import requests
from gspread import Worksheet
from data_structures.remax import RemaxDataStructure
from data_structures.worksheet_structure import WorksheetStructure
from providers.provider import Provider

class Remax(Provider):
    # Estrie = 5
    # C-du-Qc = 17

    def __init__(self, worksheet: Worksheet) -> None:
        self.regionMapping = {
            'Drummondville': 17,
            'Sherbrooke': 5
        }
        self.buildingLinks = []
        self.baseUrl = "https://www.remax-quebec.com"
        super().__init__(worksheet)
    
    def fetch_buildings(self, city):
        searchPage = requests.post(self.baseUrl + "/fr/recherche/plex/resultats.rmx", data={
            'regionIds': self.regionMapping.get(city),
            'selecItemregionIds': self.regionMapping.get(city),
        })
        soup = BeautifulSoup(searchPage.content, 'html.parser')
        pages = soup.find(class_='pagination').find_all('li')
        pagesToRequest = []
        for page in pages:
            pagesToRequest.append(self.baseUrl + page.find('a')['href'])
        
        # Keep unique values in list
        pagesToRequest = list(set(pagesToRequest))
        
        for pageLink in pagesToRequest:
            page = requests.post(pageLink, data={
                'regionIds': self.regionMapping.get(city),
                'selecItemregionIds': self.regionMapping.get(city),
            })
            soup = BeautifulSoup(page.content, 'html.parser')

            for propertyEntry in soup.find_all(class_='property-entry'):
                link = propertyEntry.find(class_='property-thumbnail')['href']
                details = propertyEntry.find(class_='property-details')
                streetAddress = details.find(class_='property-address').find(class_='property-address-street').text.replace(', ', '')
                locality = details.find(class_='property-address').find(class_='property-address-locality').text.replace(', ', '')
                
                if city in locality:
                    self.buildingLinks.append({
                        "address": streetAddress,
                        "link": self.baseUrl + link,
                        "city": locality,
                    })
    
    def export_to_worksheet(self):
        for building in self.buildingLinks:
            link = building.get('link')
            resultPage = requests.get(link)

            soup = BeautifulSoup(resultPage.content, 'html.parser')
            price = int(re.sub(r'\W+', '', soup.find(class_='Caption__Price').text.strip()))
            unitsCount = self.get_units_from_html(soup.find(class_='Caption__Title').find(class_='Caption__Name').text)
            grossRevenue = soup.find(class_='Financials__Subtitle', text='Revenus annuels bruts (potentiels)').findNext('ul').find(class_='Financials__Data').text.strip()
            taxesList = soup.find(class_='Financials__Subtitle', text='Taxes').findNext('ul').find_all(class_='Financials__Item')
            municipalTaxes = taxesList[0].find(class_='Financials__Data').text.strip() if len(taxesList) > 0 else 0 
            schoolTaxes = taxesList[1].find(class_='Financials__Data').text.strip() if len(taxesList) > 1 else 0
            #insurances = soup.find(class_='Financials__Subtitle', text='Dépenses Annuelles').findNext('ul')#.find(class_='Financials__Label', text='Assurances')
            #print(insurances)

            data = {
                'address': building.get('address'),
                'url': building.get('link'),
                'city': building.get('city'),
                'price': price,
                'units_count': unitsCount,
                'gross_revenue': int(re.sub(r'\W+', '', grossRevenue.replace(',00 $', ''))),
                'municipal_taxes': int(re.sub(r'\W+', '', municipalTaxes.replace(',00 $', ''))),
                'school_taxes': int(re.sub(r'\W+', '', schoolTaxes.replace(',00 $', ''))),
            }

            #print(data)

            print(link, resultPage.status_code)

            super().export_to_worksheet(RemaxDataStructure(data, super().get_next_empty_row()))

            # Simulate time between queries for more realism.
            time.sleep(1)

    def get_units_from_html(self, htmlText):
        if '9' in htmlText:
            return 9
        if '8' in htmlText:
            return 8
        if '7' in htmlText:
            return 7
        if '6' in htmlText:
            return 6
        if '5' in htmlText or 'Quintuplex' in htmlText:
            return 5
        if '4' in htmlText or 'Quadruplex' in htmlText:
            return 4
        if '3' in htmlText or 'Triplex' in htmlText:
            return 3
        if '2' in htmlText or 'Duplex' in htmlText:
            return 2
        
        return 0