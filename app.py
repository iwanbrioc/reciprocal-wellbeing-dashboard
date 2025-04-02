# Reciprocal Well-being AI System with Dashboard and Interactivity

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os

class Domain:
    def __init__(self, name, input_label, output_label):
        self.name = name
        self.input_label = input_label
        self.output_label = output_label
        self.input_value = 0.0
        self.output_value = 0.0

    def update(self, input_value):
        self.input_value = input_value
        self.output_value = self.calculate_output()

    def calculate_output(self):
        return self.input_value

    def __str__(self):
        return f"{self.name}: {self.input_label}={self.input_value}, {self.output_label}={self.output_value}"


class ReciprocalWellbeingSystem:
    def __init__(self):
        self.domains = [
            Domain("Environment", "Resources", "Re-enchantment"),
            Domain("Culture", "Values", "Transformation"),
            Domain("Infrastructure", "Affordance", "Creativity"),
            Domain("Society", "Support", "Dialogue"),
            Domain("Outer Self", "Capacity", "Curiosity"),
            Domain("Inner Self", "Well-being", "Participation"),
            Domain("No Self", "Everything/Nothing", "Fulfilment")
        ]

    def update_inputs(self, input_values):
        for domain, value in zip(self.domains, input_values):
            domain.update(value)

    def check_flow_blockages(self):
        blockages = []
        for domain in self.domains:
            if domain.input_value < 0.3:
                blockages.append((domain.name, domain.input_label))
        return blockages

    def get_data(self):
        return {
            "labels": [d.name for d in self.domains],
            "inputs": [d.input_value for d in self.domains],
            "outputs": [d.output_value for d in self.domains]
        }


# Streamlit Interface
st.title("Reciprocal Well-being Dashboard")
st.markdown("""
This dashboard allows you to input data for each domain of the Reciprocal Well-being Model,
view the resulting outputs, and detect areas where the system flow may be blocked.
""")

system = ReciprocalWellbeingSystem()

st.sidebar.subheader("Upload Survey Data (Optional)")
uploaded_file = st.sidebar.file_uploader("Upload CSV with domain inputs", type=["csv"])

inputs = []

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    try:
        inputs = df.iloc[0, :7].tolist()
        st.sidebar.success("Survey data loaded successfully.")
    except:
        st.sidebar.error("Invalid CSV format. Please ensure it has 7 numeric columns.")
else:
    st.subheader("Manual Input Values")
    for domain in system.domains:
        value = st.slider(f"{domain.name} ({domain.input_label})", 0.0, 1.0, 0.5, 0.01)
        inputs.append(value)

system.update_inputs(inputs)
blockages = system.check_flow_blockages()
data = system.get_data()

st.subheader("System Outputs")
fig, ax = plt.subplots(figsize=(10, 4))
x = range(len(data['labels']))
ax.bar(x, data['inputs'], width=0.4, label='Input', align='center')
ax.bar([i + 0.4 for i in x], data['outputs'], width=0.4, label='Output', align='center')
ax.set_xticks([i + 0.2 for i in x])
ax.set_xticklabels(data['labels'], rotation=45, ha='right')
ax.set_ylim(0, 1.2)
ax.legend()
st.pyplot(fig)

if blockages:
    st.subheader("Blockages Detected")
    for b in blockages:
        st.write(f"- {b[0]}: Low {b[1]}")
else:
    st.success("System Flowing Well")
