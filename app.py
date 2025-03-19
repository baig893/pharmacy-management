import streamlit as st
import pandas as pd

# Load Pharmacy Data
pharmacy_file = "pharmacy.csv"

# Title of the Web App
st.title("🏥 Pharmacy Management System")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv(pharmacy_file)

df = load_data()

# View Inventory
st.subheader("📋 View Medicine Inventory")
st.dataframe(df)

# Search Medicine
search = st.text_input("🔍 Search Medicine by Name")
if search:
    result = df[df["Name"].str.lower().str.contains(search.lower())]
    st.dataframe(result)

# Add Medicine
st.subheader("➕ Add New Medicine")
med_name = st.text_input("Medicine Name")
med_price = st.number_input("Price", min_value=0.0, format="%.2f")
med_quantity = st.number_input("Quantity", min_value=0)
med_expiry = st.date_input("Expiry Date")

if st.button("Add Medicine"):
    new_data = pd.DataFrame([{
        "Medicine ID": len(df) + 1,
        "Name": med_name,
        "Price": med_price,
        "Quantity": med_quantity,
        "Expiry Date": med_expiry
    }])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(pharmacy_file, index=False)
    st.success(f"✅ {med_name} added successfully!")

