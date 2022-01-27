import time
import re
from bs4 import BeautifulSoup
import requests
from gspread import Worksheet
from data_structures.remax import RemaxDataStructure
from data_structures.worksheet_structure import WorksheetStructure
from providers.provider import Provider

class Remax(Provider):
    def __init__(self, worksheet: Worksheet) -> None:
        self.regionMapping = {
            'Drummondville': 17,
            'Sherbrooke': 5
        }
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

        existingLinks = self.get_existing_links()
        
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
                
                if city in locality and self.baseUrl + link not in existingLinks:
                    self.buildingLinks.append({
                        "address": streetAddress,
                        "link": self.baseUrl + link,
                        "city": city,
                    })
    
    def export_to_worksheet(self):
        for building in self.buildingLinks:
            link = building.get('link')
            resultPage = requests.get(link)

            print(link, resultPage.status_code)

            soup = BeautifulSoup(resultPage.content, 'html.parser')
            price = self.format_money_string_to_int(soup.find(class_='Caption__Price').text.strip())
            unitsCount = self.get_units_from_html(soup.find(class_='Caption__Title').find(class_='Caption__Name').text)
            grossRevenue = soup.find(class_='Financials__Subtitle', text='Revenus annuels bruts (potentiels)').findNext('ul').find(class_='Financials__Data').text.strip()
            
            taxesDiv = soup.find(class_='Financials__Subtitle', text='Taxes').findNext('ul')
            taxes = self.get_taxes_html(taxesDiv)

            annualExpensesDiv = soup.find(class_='Financials__Subtitle', text='Dépenses Annuelles')
            insurances = self.get_insurance_html(annualExpensesDiv)

            # We check for only 'nergie' because I'm not sure that the first letter is capital or not and with accent or not.
            energyDiv = soup.find(class_='Financials__Subtitle', text=lambda t : 'nergie' in t)
            energy = self.get_energy(energyDiv)
            

            data = {
                'address': building.get('address'),
                'url': building.get('link'),
                'city': building.get('city'),
                'price': price,
                'units_count': unitsCount,
                'gross_revenue': self.format_money_string_to_int(grossRevenue),
                'municipal_taxes': self.format_money_string_to_int(taxes[0]),
                'school_taxes': self.format_money_string_to_int(taxes[1]),
                'insurances': self.format_money_string_to_int(insurances),
                'energy': energy
            }

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
    
    def get_insurance_html(self, annualExpenses):
        insurances = "0"
        if annualExpenses is not None:
            insurancesHtml = annualExpenses.findNext('ul').find(class_='Financials__Label', text=lambda t : 'Assurances' in t)
            if insurancesHtml is not None:
                insurances = insurancesHtml.findNext(class_='Financials__Data').text.strip()
        return insurances
    
    def get_taxes_html(self, taxesDiv):
        municipalTaxes = "0"
        schoolTaxes = "0"

        municipalTaxesLabel = taxesDiv.find(class_='Financials__Label', text=lambda t : 'Taxes municipales' in t)
        if municipalTaxesLabel is not None:
            municipalTaxes = municipalTaxesLabel.findNext(class_='Financials__Data').text.strip() 
        
        schoolTaxesLabel = taxesDiv.find(class_='Financials__Label', text=lambda t : 'Taxes scolaires' in t)
        if schoolTaxesLabel is not None:
            schoolTaxes = schoolTaxesLabel.findNext(class_='Financials__Data').text.strip()
        
        return (municipalTaxes, schoolTaxes)
    
    def get_energy(self, energyDiv):
        energySum = 0
        if energyDiv is not None:
            energyItems = energyDiv.findNext('ul').find_all(class_='Financials__Item')
            if len(energyItems) > 0:
                for energyItem in energyItems:
                    energySum += self.format_money_string_to_int(energyItem.find(class_='Financials__Data').text.strip())
        return energySum
    
    def format_money_string_to_int(self, text):
        return int(re.sub(r'\D+', '', text.replace(',00 $', '').replace(' ', '')))