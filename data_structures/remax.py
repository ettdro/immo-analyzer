from data_structures.worksheet_structure import WorksheetStructure


class RemaxDataStructure(WorksheetStructure):
    def __init__(self, jsonData, row) -> None:
        self.jsonData = jsonData
        super().__init__(row)
    
    def get_address(self):
        return self.jsonData.get('address')
    
    def get_url(self):
        return self.jsonData.get('url')
    
    def get_city(self):
        return self.jsonData.get('city')
    
    def get_price(self):
        return self.jsonData.get('price')
    
    def get_units_count(self):
        return self.jsonData.get('units_count')
    
    def get_unit_types(self):
        return "" # Can't find it on Remax website
    
    def get_potential_gross_income(self):
        return self.jsonData.get('gross_revenue')
    
    def get_municipal_taxes(self):
        return self.jsonData.get('municipal_taxes')

    def get_school_taxes(self):
        return self.jsonData.get('school_taxes')

    def get_insurances_price(self):
        return 0#self.jsonData.get('fAssurances')

    def get_energy_price(self):
        return 0#self.jsonData.get('fElectricite')