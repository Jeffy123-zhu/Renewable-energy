# =====================================================
# energy_model.py
# Independent Energy Analysis & CO2 Prediction Project
# Core functions for loading energy data and predicting CO2
# =====================================================

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
np.random.seed(42)

def load_energy_data(csv_path=None):
    """
    Load energy data from CSV or generate simulated data if CSV not found.
    Calculates renewable fraction, energy efficiency, CO2, optimized CO2, and predicted CO2.
    Returns a DataFrame with all metrics.
    """
    if csv_path:
        try:
            energy_data = pd.read_csv(csv_path)
        except:
            csv_path = None
    if not csv_path:
        months = np.arange(1,13)
        total_energy = np.random.randint(200,500,12)
        solar_energy = np.random.randint(50,150,12)
        wind_energy = np.random.randint(30,100,12)
        energy_data = pd.DataFrame({
            "Month": months,
            "Total_Energy": total_energy,
            "Solar": solar_energy,
            "Wind": wind_energy
        })

    total_renewable = energy_data["Solar"] + energy_data["Wind"]
    energy_data["Renewable_Fraction"] = np.where(
        energy_data["Total_Energy"]>0, total_renewable/energy_data["Total_Energy"], 0.0)
    energy_data["Energy_Efficiency"] = np.where(
        total_renewable>0, energy_data["Total_Energy"]/total_renewable, np.nan)
    energy_data["CO2"] = energy_data["Total_Energy"] * 0.5
    energy_data["CO2_after_opt"] = energy_data["CO2"] * (1-energy_data["Renewable_Fraction"])

    X = energy_data[["Month"]]
    y = energy_data["CO2"]
    co2_model = LinearRegression().fit(X,y)
    energy_data["CO2_predicted"] = co2_model.predict(X)

    return energy_data

def predict_CO2(total_energy, solar, wind, month):
    """
    Predict CO2 and calculate renewable fraction & energy efficiency for a single input.
    Returns a dictionary of metrics rounded to 2 decimals.
    """
    renewable_fraction = (solar+wind)/total_energy if total_energy>0 else 0
    energy_efficiency = total_energy/(solar+wind) if (solar+wind)>0 else np.nan
    co2_original = total_energy*0.5
    co2_after_opt = co2_original*(1-renewable_fraction)
    co2_predicted = co2_original  # simplified linear prediction for demonstration

    return {
        "CO2_Original": round(co2_original,2),
        "CO2_After_Optimization": round(co2_after_opt,2),
        "CO2_Predicted": round(co2_predicted,2),
        "Renewable_Fraction": round(renewable_fraction,2),
        "Energy_Efficiency": round(energy_efficiency,2)
    }
