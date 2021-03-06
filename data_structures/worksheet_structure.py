from abc import ABC, abstractmethod
from gspread.utils import rowcol_to_a1

class WorksheetStructure(ABC):
    def __init__(self, row) -> None:
        self.row = row
        self.colsIndex = dict({
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
            'joint_tga': 38,
            'jvm': 39,
            'deal_or_no_deal': 40,
            'break_even': 41,
            'coc': 42,
            'profitability_treshold': 43,
            'jvm_purchase': 44,
            'investment_per_unit': 45,
            'potential_raise_per_unit': 46,
            'total_investment': 47,
            'net_revenue_after_optimisation': 48,
            'value_after_optimisation': 49,
            'value_creation_potential': 50,
            'real_value_creation': 51,
            'refinance_mortgage': 52,
            'refinancing_proceeds': 53,
            'rcd': 54
        })

        self.vacancyEstimateCell = "$%s$1" % (self.get_static_cell('vacancy'))
        self.janitorEstimateCell = "$%s$1" % (self.get_static_cell('janitor'))
        self.maintenanceEstimateCell = "$%s$1" % (self.get_static_cell('maintenance'))
        self.managementEstimateCell = "$%s$1" % (self.get_static_cell('management'))
        self.mortgageEstimateCell = "$%s$1" % (self.get_static_cell('mortgage'))
        self.capitalisationEstimateCell = "$%s$1" % (self.get_static_cell('capitalisation'))
        self.hypotheticalEstimateCell = "$%s$1" % (self.get_static_cell('hypothetical_appreciation'))
        self.jointTgaEstimateCell = "$%s$1" % (self.get_static_cell('joint_tga'))
        self.cashOnCashEstimateCell = "$%s$1" % (self.get_static_cell('coc'))
        self.refinanceMortgageEstimateCell = "$%s$1" % (self.get_static_cell('refinance_mortgage'))
    
    def get_static_cell(self, name):
        return ''.join(filter(str.isalpha, rowcol_to_a1(1, self.colsIndex.get(name))))

    def get_cell_value(self, name):
        return rowcol_to_a1(self.row, self.colsIndex.get(name))

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

    def get_price_per_unit(self):
        return "=%s/%s" % (self.get_cell_value('price'), self.get_cell_value('units_count'))

    def get_avg_monthly_rent(self):
        return "=%s/12/%s" % (self.get_cell_value('gross_revenue'), self.get_cell_value('units_count'))
    
    def get_rents_price_diff_in_sector(self):
        return "=if(%s>'Donn??es sur loyer'!$E$7,\"above\",\"below\")" % (self.get_cell_value('avg_unit_price'))
    
    def get_normalized_net_revenues(self):
        return "=%s-%s" % (self.get_cell_value('gross_revenue'), self.get_cell_value('normalized_expenses'))
    
    def get_tga(self):
        return "=%s/%s" % (self.get_cell_value('net_revenue'), self.get_cell_value('price'))
    
    def get_delta_per_unit(self):
        return "=%s-%s" % (self.get_cell_value('new_construct_value'), self.get_cell_value('price_per_unit'))
    
    def get_delta_new_construction(self):
        return "=%s*%s" % (self.get_cell_value('delta_per_unit'), self.get_cell_value('units_count'))
    
    def get_renovation_price(self):
        return "=if(%s<125000,80000,0)" % (self.get_cell_value('price_per_unit'))
    
    def get_profit_per_unit(self):
        return "=%s-%s" % (self.get_cell_value('delta_per_unit'), self.get_cell_value('renovation'))
    
    def get_value_creation(self):
        return "=%s*%s" % (self.get_cell_value('profit_per_unit'), self.get_cell_value('units_count'))
    
    def get_normalized_expenses(self):
        return "=SUM(%s:%s)" % (self.get_cell_value('municipal_taxes'), self.get_cell_value('management'))
    
    def get_total_expenses(self):
        return "=%s+%s" % (self.get_cell_value('normalized_expenses'), self.get_cell_value('mortgage'))
    
    def get_expenses_percentage(self):
        return "=%s/%s" % (self.get_cell_value('normalized_expenses'), self.get_cell_value('gross_revenue'))
    
    def get_janitor_expenses(self):
        return "=if(%s<8, (%s*%s), (330*%s))" % (self.get_cell_value('units_count'), self.janitorEstimateCell, self.get_cell_value('units_count'), self.get_cell_value('units_count'))
    
    def get_vacancy(self):
        return "=%s*%s" % (self.vacancyEstimateCell, self.get_cell_value('gross_revenue'))
    
    def get_annual_maintenance(self):
        return "=%s*%s" % (self.maintenanceEstimateCell, self.get_cell_value('units_count'))
    
    def get_annual_management(self):
        return "=%s*%s*%s*12" % (self.managementEstimateCell, self.get_cell_value('avg_unit_price'), self.get_cell_value('units_count'))
    
    def get_annual_mortgage(self):
        return "=-pmt(%s/12,30*12,(%s-%s))*12" % (self.mortgageEstimateCell, self.get_cell_value('price'), self.get_cell_value('downpayment'))
    
    def get_downpayment(self):
        return "=if(%s>4,0.15*%s,0.25*%s)" % (self.get_cell_value('units_count'), self.get_cell_value('price'), self.get_cell_value('price'))
    
    def get_cashflow_before_taxes(self):
        return "=%s-%s" % (self.get_cell_value('gross_revenue'), self.get_cell_value('total'))
    
    def get_capitalisation_before_taxes(self):
        return "=%s*%s" % (self.get_cell_value('mortgage'), self.capitalisationEstimateCell)
    
    def get_total_non_speculative(self):
        return "=%s+%s" % (self.get_cell_value('cashflow'), self.get_cell_value('capitalisation'))
    
    def get_bi_factor_return(self):
        return "=%s/%s" % (self.get_cell_value('non_speculative_total'), self.get_cell_value('downpayment'))
    
    def get_hypothetical_appreciation(self):
        return "=%s*%s" % (self.hypotheticalEstimateCell, self.get_cell_value('price'))
    
    def get_tri_factor_return(self):
        return "=(%s+%s)/%s" % (self.get_cell_value('hypothetical_appreciation'), self.get_cell_value('non_speculative_total'), self.get_cell_value('downpayment'))
    
    def get_joint_tga(self):
        return "=%s" % self.jointTgaEstimateCell

    def get_jvm(self):
        return "=(%s-%s+%s)/%s" % (
            self.get_cell_value('gross_revenue'),
            self.get_cell_value('total'),
            self.get_cell_value('mortgage'),
            self.get_cell_value('joint_tga')
        )
    
    def get_deal_or_no_deal(self):
        return "=%s-%s" % (self.get_cell_value('price'), self.get_cell_value('jvm'))
    
    def get_break_even(self):
        return "=-%s/%s/12" % (self.get_cell_value('cashflow'), self.get_cell_value('units_count'))
    
    def get_cash_on_cash(self):
        return "=(%s*%s)/12/%s" % (self.get_cell_value('downpayment'), self.cashOnCashEstimateCell, self.get_cell_value('units_count'))
    
    def get_profitability_treshold(self):
        return "=%s+%s" % (self.get_cell_value('break_even'), self.get_cell_value('coc'))
    
    def get_jvm_purchase(self):
        return "=%s/%s" % (self.get_cell_value('net_revenue'), self.get_cell_value('joint_tga'))

    def get_value_after_optimisation(self):
        return "=%s/%s" % (self.get_cell_value('net_revenue_after_optimisation'), self.get_cell_value('joint_tga'))
    
    def get_net_revenue_after_optimisation(self):
        return "=%s+(%s*12*%s)" % (self.get_cell_value('net_revenue'), self.get_cell_value('potential_raise_per_unit'), self.get_cell_value('units_count'))
    
    def get_value_creation_potential(self):
        return "=%s-%s-%s" % (self.get_cell_value('value_after_optimisation'), self.get_cell_value('jvm_purchase'), self.get_cell_value('total_investment'))
    
    def get_real_value_creation(self):
        return "=%s-%s" % (self.get_cell_value('value_after_optimisation'), self.get_cell_value('price'))
    
    def get_refinance_mortgage(self):
        return "=%s*%s" % (self.get_cell_value('value_after_optimisation'), self.refinanceMortgageEstimateCell)
    
    def get_refinancing_proceeds(self):
        return "=%s-(%s-%s)-%s" % (
            self.get_cell_value('refinance_mortgage'),
            self.get_cell_value('price'),
            self.get_cell_value('downpayment'),
            self.get_cell_value('total_investment')
        )
    
    def get_rcd(self):
        return "=(%s-%s)/%s" % (self.get_cell_value('gross_revenue'), self.get_cell_value('normalized_expenses'), self.get_cell_value('mortgage'))
