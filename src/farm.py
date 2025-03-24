from src.fund import Fund
import simpy as sp
from src.parameters import FarmParameters, FarmPlotParameters, ConversionParameters


class FarmingBusiness:
    def __init__(self,
                 env: sp.Environment,
                 fund: Fund,
                 plot_params: FarmPlotParameters,
                 farm_params: FarmParameters,
                 conversion_params: ConversionParameters):
        self.fund = fund
        self.plot_params = plot_params
        self.farm_params = farm_params
        self.conversion_params = conversion_params
        self.date = 0
        self.env = env
        self.total_energy_cost = 0
        self.current_growth_per_plot = 0
        self.total_kg_product_made = 0
        self.unsold_kg_product = 0
        plots_per_floor = int(
            self.farm_params.total_floor_m_squared /
            self.plot_params.floor_m_squared)
        if self.plot_params.stackable:
            floors = int(self.farm_params.floor_height /
                         self.plot_params.height_m)
            self.plot_count = int(plots_per_floor * floors)
        else:
            self.plot_count = plots_per_floor

        self.transport_event = self.env.event()

        self.initial_setup()

        self.env.process(self.on_day())
        self.env.process(self.transport())
        self.env.process(self.rent())

    def initial_setup(self):
        plot_setup_cost = self.farm_params.setup_cost_m_squared_usd * \
            self.plot_count * self.plot_params.floor_m_squared
        self.fund.withdraw(plot_setup_cost)
        if not self.farm_params.is_renting:
            farm_land_cost = self.farm_params.total_floor_m_squared * \
                self.conversion_params.m_squared_market_price
            self.fund.withdraw(farm_land_cost)
        self.fund_history = [self.fund.balance]

    def rent(self):
        while True:
            yield self.env.timeout(365 / 12)
            if self.farm_params.is_renting:
                rent_cost = self.farm_params.total_floor_m_squared * \
                    self.conversion_params.m_squared_rent_usd
                self.fund.withdraw(rent_cost)

    def transport(self):
        while True:
            yield self.transport_event

            self.unsold_kg_product -= self.farm_params.kg_before_transport

            transport_cost = self.farm_params.km_to_customer * \
                self.conversion_params.km_to_usd
            transport_energy_cost = self.farm_params.km_to_customer * \
                self.conversion_params.km_to_energy
            transport_cost += transport_energy_cost * \
                self.conversion_params.energy_to_usd

            self.fund.withdraw(transport_cost)

            sales_usd = self.farm_params.kg_before_transport * \
                self.conversion_params.kg_product_to_usd

            self.fund.deposit(sales_usd)

            self.total_energy_cost += transport_energy_cost

            self.transport_event = self.env.event()

    def on_day(self):
        while True:
            yield self.env.timeout(1)
            day_energy_cost = 0
            day_earnings = 0
            self.fund.on_pass_days(1)

            energy_cost_per_plot = self.plot_params.temp_control_energy_cost
            energy_cost_per_plot += self.plot_params.air_control_energy_cost

            day_earnings -= self.plot_params.labour_cost_usd * self.plot_count
            if not self.plot_params.captures_rainwater:
                day_earnings -= self.plot_params.water_cost_L * \
                    self.plot_count * self.conversion_params.water_L_to_usd

            if self.plot_params.captures_sunlight:
                if self.env.now % 365 < self.farm_params.growing_period_days:
                    self.current_growth_per_plot += 1
            else:
                self.current_growth_per_plot += 1

            day_energy_cost += energy_cost_per_plot * self.plot_count

            day_earnings -= day_energy_cost * \
                self.conversion_params.energy_to_usd
            self.total_energy_cost += day_energy_cost
            if self.current_growth_per_plot > \
                    self.plot_params.growth_to_harvest:
                self.current_growth_per_plot = 0
                harvest_kg = self.plot_params.harvest_kg_product_output * \
                    self.plot_count
                self.unsold_kg_product += harvest_kg
                self.total_kg_product_made += harvest_kg

            if self.unsold_kg_product >= self.farm_params.kg_before_transport:
                self.transport_event.succeed()

            self.total_energy_cost += day_energy_cost

            self.fund.deposit(day_earnings)
            self.fund_history.append(self.fund.balance)
