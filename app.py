# =====================================================
# app.py
# Streamlit Web App for Independent Energy Analysis & CO2 Prediction Project
# =====================================================

import streamlit as st
import matplotlib.pyplot as plt
from energy_model import load_energy_data, predict_CO2

st.set_page_config(page_title="Energy & CO2 Analysis", layout="wide")
st.title("Independent Energy Analysis & CO2 Prediction Project")
st.markdown("""
This project demonstrates independent development skills:
- Data loading, cleaning, and validation
- Renewable fraction & energy efficiency calculation
- CO2 estimation, optimization, and simple linear prediction
- Interactive visualizations
""")

# ---------------------------
# Sidebar: User Input for Prediction
# ---------------------------
st.sidebar.header("Input Energy Data")
total_energy = st.sidebar.number_input("Total Energy (kWh)", value=300, min_value=0)
solar = st.sidebar.number_input("Solar Energy (kWh)", value=100, min_value=0)
wind = st.sidebar.number_input("Wind Energy (kWh)", value=50, min_value=0)
month = st.sidebar.slider("Month", 1,12,1)

# Predict CO2 when user clicks button
if st.button("Predict CO2 & Metrics"):
    metrics = predict_CO2(total_energy, solar, wind, month)
    st.subheader("Prediction Results")
    st.json(metrics)

# ---------------------------
# Load yearly energy data
# ---------------------------
energy_data = load_energy_data()

# ---------------------------
# Visualization 1: Total & Renewable Energy
# ---------------------------
st.subheader("Monthly Total & Renewable Energy")
fig, ax = plt.subplots(figsize=(8,4))
ax.plot(energy_data["Month"], energy_data["Total_Energy"], marker='o', label="Total Energy")
ax.plot(energy_data["Month"], energy_data["Solar"], marker='o', label="Solar Energy")
ax.plot(energy_data["Month"], energy_data["Wind"], marker='o', label="Wind Energy")
ax.set_xlabel("Month")
ax.set_ylabel("Energy (kWh)")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# ---------------------------
# Visualization 2: CO2 Emissions
# ---------------------------
st.subheader("CO2 Emissions: Original vs Optimized vs Predicted")
fig2, ax2 = plt.subplots(figsize=(8,4))
ax2.plot(energy_data["Month"], energy_data["CO2"], marker='o', label="Original CO2")
ax2.plot(energy_data["Month"], energy_data["CO2_after_opt"], marker='o', linestyle='--', label="Optimized CO2")
ax2.plot(energy_data["Month"], energy_data["CO2_predicted"], marker='x', linestyle=':', label="Predicted CO2")
ax2.set_xlabel("Month")
ax2.set_ylabel("CO2")
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)

# ---------------------------
# Visualization 3: Renewable Fraction
# ---------------------------
st.subheader("Monthly Renewable Fraction (%)")
fig3, ax3 = plt.subplots(figsize=(8,4))
ax3.bar(energy_data["Month"], energy_data["Renewable_Fraction"]*100, color="green", alpha=0.7)
ax3.set_xlabel("Month")
ax3.set_ylabel("Renewable Fraction (%)")
ax3.set_ylim(0,100)
ax3.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig3)

# ---------------------------
# Analysis Notes
# ---------------------------
max_renewable_idx = energy_data["Renewable_Fraction"].idxmax()
max_co2_idx = energy_data["CO2"].idxmax()
avg_fraction = energy_data["Renewable_Fraction"].mean()

st.markdown(f"""
**Month with highest renewable fraction:** {energy_data.loc[max_renewable_idx,'Month']} ({energy_data.loc[max_renewable_idx,'Renewable_Fraction']:.2f})  
**Month with highest CO2 emission:** {energy_data.loc[max_co2_idx,'Month']} ({energy_data.loc[max_co2_idx,'CO2']:.1f})  
**Average renewable fraction over the year:** {avg_fraction:.2f}  

*Observation:* Renewable share varies month to month, and CO2 decreases when renewables are high.  
*Social value:* This model helps forecast CO2 emission trends and optimize energy planning.
""")
