from abc import ABC, abstractmethod
from gspread.utils import ValueInputOption
from gspread import Worksheet

from data_structures.worksheet_structure import WorksheetStructure

class Provider(ABC):
    def __init__(self, worksheet: Worksheet) -> None:
        self.worksheet = worksheet

    @abstractmethod
    def fetch_buildings(self, city):
        pass

    @abstractmethod
    def export_to_worksheet(self, structure: WorksheetStructure):
        self.worksheet.insert_row([
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
            structure.get_deal_or_no_deal(),
            structure.get_break_even(),
            structure.get_cash_on_cash(),
            structure.get_profitability_treshold(),
            structure.get_jvm_purchase(),
            "", # manual inputs
            "", # manual inputs
            "", # manual inputs
            structure.get_net_revenue_after_optimisation(),
            structure.get_value_after_optimisation(),
            structure.get_value_creation_potential(),
            structure.get_real_value_creation(),
            structure.get_refinance_mortgage(),
            structure.get_refinancing_proceeds(),
            structure.get_rcd()
        ], structure.row, ValueInputOption.user_entered)
    
    def get_next_empty_row(self):
        initialRow = 3
        values = self.worksheet.get_values('A' + str(initialRow) + ':A')

        if values == []:
            return initialRow
        
        return initialRow + len(values);