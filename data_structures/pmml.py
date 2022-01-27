from data_structures.worksheet_structure import WorksheetStructure


class PmmlDataStructure(WorksheetStructure):
    def __init__(self, jsonData, row) -> None:
        self.jsonData = jsonData
        super().__init__(row)
    
    def get_address(self):
        return '=HYPERLINK("%s", "%s %s")' % (self.get_url(), self.jsonData.get('sNumeroCivique'), self.jsonData.get('sRue'))
    
    def get_url(self):
        return "https://goplex.com/{}".format(self.jsonData.get('sLien'))
    
    def get_city(self):
        return self.jsonData.get('sNomVille')
    
    def get_price(self):
        return self.jsonData.get('fPrixDemande')
    
    def get_units_count(self):
        return self.jsonData.get('iUnitesTotal')
    
    def get_unit_types(self):
        return self.jsonData.get('sRepartition')
    
    def get_potential_gross_income(self):
        return self.jsonData.get('fTotalRevenu')
    
    def get_municipal_taxes(self):
        return self.jsonData.get('fTaxesMunicipales')

    def get_school_taxes(self):
        return self.jsonData.get('fTaxesScolaires')

    def get_insurances_price(self):
        return self.jsonData.get('fAssurances')

    def get_energy_price(self):
        return self.jsonData.get('fElectricite')
    
    
