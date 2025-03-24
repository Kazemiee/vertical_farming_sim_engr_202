from dataclasses import dataclass


@dataclass
class FarmPlotParameters:
    light_energy_needed: float = 1
    nutrient_cost_g: float = 10
    water_cost_L: float = 0.1
    labour_cost_usd: float = 0.00001
    temp_control_energy_cost: float = 0
    air_control_energy_cost: float = 0
    growth_to_harvest: float = 30
    harvest_kg_product_output: float = 0.03123
    floor_m_squared: float = 0.03
    height_m: float = 1.3
    stackable: bool = False
    captures_sunlight: bool = True
    captures_rainwater: bool = True


@dataclass
class FarmParameters:
    total_floor_m_squared: float = 100 * 100
    floor_height: float = 10
    is_renting: bool = True
    growing_period_days: float = 365
    kg_before_transport: float = 15000
    km_to_customer: float = 2500
    setup_cost_m_squared_usd: float = 1


@dataclass
class ConversionParameters:
    kg_product_to_usd: float = 15
    energy_to_usd: float = 0.01
    g_nutrient_to_usd: float = 0.01
    m_squared_rent_usd: float = 10
    m_squared_market_price: float = 2000
    water_L_to_usd: float = 0.00000004
    km_to_energy: float = 1
    km_to_usd: float = 1
