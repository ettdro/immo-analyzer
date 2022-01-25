from abc import ABC, abstractmethod
from gspread.utils import rowcol_to_a1

class WorksheetStructure(ABC):
    def __init__(self) -> None:
        self.rowsIndex = dict({
            'address': 1,
            'url': 2,
            'city': 3,
            'price': 4,
            'downpayment': 5,
            'units_count': 6,
            'unit_types': 7,
            'price_per_unit': 8,
            'gross_revenue': 9,
            'avg_unit_price': 10,
            'diff_in_sector': 11,
            'net_revenue': 12,
            'tga': 13,
            'new_construct_value': 14,
            'delta_per_unit': 15,
            'delta_new_construct': 16,
            'renovation': 17,
            'profit_per_unit': 18,
            'value_creation': 19,
            'municipal_taxes': 20,
            'school_taxes': 21,
            'insurances': 22,
            'energy': 23,
            'janitor': 24,
            'vacancy': 25,
            'maintenance': 26,
            'management': 27,
            'normalized_expenses': 28,
            'mortgage': 29,
            'total': 30,
            'expenses_percentage': 31,
            'cashflow': 32,
            'capitalisation': 33,
            'non_speculative_total': 34,
            'bi_factor_return': 35,
            'hypothetical_appreciation': 36,
            'tri_factor_return': 37,
            'jvm': 38
        })
        self.vacancyEstimateCell = "$A$%s" % (self.rowsIndex.get('vacancy'))
        self.janitorEstimateCell = "$A$%s" % (self.rowsIndex.get('janitor'))
        self.maintenanceEstimateCell = "$A$%s" % (self.rowsIndex.get('maintenance'))
        self.managementEstimateCell = "$A$%s" % (self.rowsIndex.get('management'))
        self.mortgageEstimateCell = "$A$%s" % (self.rowsIndex.get('mortgage'))
        self.capitalisationEstimateCell = "$A$%s" % (self.rowsIndex.get('capitalisation'))
        self.hypotheticalEstimateCell = "$A$%s" % (self.rowsIndex.get('hypothetical_appreciation'))

    @abstractmethod
    def get_address(self):
        pass

    @abstractmethod
    def get_url(self):
        pass

    @abstractmethod
    def get_city(self):
        pass

    @abstractmethod
    def get_price(self):
        pass

    @abstractmethod
    def get_units_count(self):
        pass

    @abstractmethod
    def get_unit_types(self):
        pass

    @abstractmethod
    def get_potential_gross_income(self):
        pass

    @abstractmethod
    def get_municipal_taxes(self):
        pass

    @abstractmethod
    def get_school_taxes(self):
        pass

    @abstractmethod
    def get_insurances_price(self):
        pass

    @abstractmethod
    def get_energy_price(self):
        pass

    def get_price_per_unit(self, col):
        return "=%s/%s" % (rowcol_to_a1(self.rowsIndex.get('price'), col), rowcol_to_a1(self.rowsIndex.get('units_count'), col))

    def get_avg_monthly_rent(self, col):
        return "=%s/12/%s" % (rowcol_to_a1(self.rowsIndex.get('gross_revenue'), col), rowcol_to_a1(self.rowsIndex.get('units_count'), col))
    
    def get_rents_price_diff_in_sector(self, col):
        return "=if(%s>'Données sur loyer'!$E$7,\"above\",\"below\")" % (rowcol_to_a1(self.rowsIndex.get('avg_unit_price'), col))
    
    def get_normalized_net_revenues(self, col):
        return "=%s-%s" % (rowcol_to_a1(self.rowsIndex.get('gross_revenue'), col), rowcol_to_a1(self.rowsIndex.get('normalized_expenses'), col))
    
    def get_tga(self, col):
        return "=%s/%s" % (rowcol_to_a1(self.rowsIndex.get('net_revenue'), col), rowcol_to_a1(self.rowsIndex.get('price'), col))
    
    def get_delta_per_unit(self, col):
        return "=%s-%s" % (rowcol_to_a1(self.rowsIndex.get('new_construct_value'), col), rowcol_to_a1(self.rowsIndex.get('price_per_unit'), col))
    
    def get_delta_new_construction(self, col):
        return "=%s*%s" % (rowcol_to_a1(self.rowsIndex.get('delta_per_unit'), col), rowcol_to_a1(self.rowsIndex.get('units_count'), col))
    
    def get_renovation_price(self, col):
        return "=if(%s<125000,80000,0)" % (rowcol_to_a1(self.rowsIndex.get('price_per_unit'), col))
    
    def get_profit_per_unit(self, col):
        return "=%s-%s" % (rowcol_to_a1(self.rowsIndex.get('delta_per_unit'), col), rowcol_to_a1(self.rowsIndex.get('renovation'), col))
    
    def get_value_creation(self, col):
        return "=%s*%s" % (rowcol_to_a1(self.rowsIndex.get('profit_per_unit'), col), rowcol_to_a1(self.rowsIndex.get('units_count'), col))
    
    def get_normalized_expenses(self, col):
        return "=SUM(%s:%s)" % (rowcol_to_a1(self.rowsIndex.get('municipal_taxes'), col), rowcol_to_a1(self.rowsIndex.get('management'), col))
    
    def get_total_expenses(self, col):
        return "=%s+%s" % (rowcol_to_a1(self.rowsIndex.get('normalized_expenses'), col), rowcol_to_a1(self.rowsIndex.get('mortgage'), col))
    
    def get_expenses_percentage(self, col):
        return "=%s/%s" % (rowcol_to_a1(self.rowsIndex.get('normalized_expenses'), col), rowcol_to_a1(self.rowsIndex.get('gross_revenue'), col))
    
    def get_janitor_expenses(self, col):
        return "=if(%s>8, (%s*%s), 0)" % (rowcol_to_a1(self.rowsIndex.get('units_count'), col), self.janitorEstimateCell, rowcol_to_a1(self.rowsIndex.get('units_count'), col))
    
    def get_vacancy(self, col):
        return "=%s*%s" % (self.vacancyEstimateCell, rowcol_to_a1(self.rowsIndex.get('gross_revenue'), col))
    
    def get_annual_maintenance(self, col):
        return "=%s*%s" % (self.maintenanceEstimateCell, rowcol_to_a1(self.rowsIndex.get('units_count'), col))
    
    def get_annual_management(self, col):
        return "=%s*%s*%s*12" % (self.managementEstimateCell, rowcol_to_a1(self.rowsIndex.get('avg_unit_price'), col), rowcol_to_a1(self.rowsIndex.get('units_count'), col))
    
    def get_annual_mortgage(self, col):
        return "=-pmt(%s/12,30*12,(%s-%s))*12" % (self.mortgageEstimateCell, rowcol_to_a1(4, col), rowcol_to_a1(self.rowsIndex.get('units_count'), col))
    
    def get_downpayment(self, col):
        return "=if(%s>4,0.15*%s,0.25*%s)" % (rowcol_to_a1(self.rowsIndex.get('units_count'), col), rowcol_to_a1(self.rowsIndex.get('price'), col), rowcol_to_a1(self.rowsIndex.get('price'), col))
    
    def get_cashflow_before_taxes(self, col):
        return "=%s-%s" % (rowcol_to_a1(self.rowsIndex.get('gross_revenue'), col), rowcol_to_a1(self.rowsIndex.get('total'), col))
    
    def get_capitalisation_before_taxes(self, col):
        return "=%s*%s" % (rowcol_to_a1(self.rowsIndex.get('mortgage'), col), self.capitalisationEstimateCell)
    
    def get_total_non_speculative(self, col):
        return "=%s+%s" % (rowcol_to_a1(self.rowsIndex.get('cashflow'), col), rowcol_to_a1(self.rowsIndex.get('capitalisation'), col))
    
    def get_bi_factor_return(self, col):
        return "=%s/%s" % (rowcol_to_a1(self.rowsIndex.get('non_speculative_total'), col), rowcol_to_a1(self.rowsIndex.get('downpayment'), col))
    
    def get_hypothetical_appreciation(self, col):
        return "=%s*%s" % (self.hypotheticalEstimateCell, rowcol_to_a1(self.rowsIndex.get('price'), col))
    
    def get_tri_factor_return(self, col):
        return "=(%s+%s)/%s" % (rowcol_to_a1(self.rowsIndex.get('hypothetical_appreciation'), col), rowcol_to_a1(self.rowsIndex.get('non_speculative_total'), col), rowcol_to_a1(self.rowsIndex.get('downpayment'), col))
    
    def get_jvm(self, col):
        return "=(%s-%s+%s)/%s" % (
            rowcol_to_a1(self.rowsIndex.get('gross_revenue'), col),
            rowcol_to_a1(self.rowsIndex.get('total'), col),
            rowcol_to_a1(self.rowsIndex.get('mortgage'), col),
            rowcol_to_a1(self.rowsIndex.get('mortgage'), col)
        )