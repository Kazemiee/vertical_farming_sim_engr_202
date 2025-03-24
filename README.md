# vertical_farming_sim_engr_202

Code to simulate the inputs and outputs of various farms.

1. Create virtual environment

   ```sh
   python -m venv .env

   ```

2. Activate python virtual environment

   ```sh
   .\.env\Scripts\Activate # Command for windows

   ```

3. Install dependencies

   ```sh
   pip install -r requirements.txt

   ```

Parameters can be tuned by changing properties of FarmParameters, FarmPlotParameters, ConversionParameters before passing them into the FarmingBusiness. To run a FarmingBusiness, call run() on the simpy.Environment passed into the FarmingBusiness.
