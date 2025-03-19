import streamlit as st
import pandas as pd

# Set page title & icon
st.set_page_config(page_title="Pharmacy Management", page_icon="💊", layout="wide")

# Custom CSS for UI enhancements
st.markdown("""
    <style>
        body { font-family: Arial, sans-serif; }
        .big-font { font-size:20px !important; font-weight: bold; }
        .stTextInput, .stNumberInput, .stDateInput {
            border-radius: 10px !important; background-color: #f5f5f5;
        }
        .stButton>button { background-color: #4CAF50; color: white; border-radius: 10px; }
        .stButton>button:hover { background-color: #45a049; }
        .success { color: #4CAF50; font-weight: bold; }
        .error { color: #FF5733; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Load existing medicine data (or create a new DataFrame)
try:
    df = pd.read_csv("pharmacy_inventory.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["Medicine ID", "Name", "Price", "Quantity", "Expiry Date"])

# Title
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>💊 Pharmacy Management System</h1>", unsafe_allow_html=True)

# Search Medicine Section
st.subheader("🔍 Search Medicine by Name")
search_query = st.text_input("Enter medicine name:", "").strip().lower()

if search_query:
    filtered_df = df[df["Name"].str.lower().str.contains(search_query)]
    if not filtered_df.empty:
        st.write(filtered_df)
    else:
        st.markdown("<p class='error'>⚠️ No medicine found!</p>", unsafe_allow_html=True)

# Display Medicine Inventory
st.subheader("📋 View Medicine Inventory")
st.dataframe(df, use_container_width=True)

# Add New Medicine Section
st.subheader("➕ Add New Medicine")
with st.form("add_medicine_form"):
    med_id = st.number_input("Medicine ID", min_value=1, step=1)
    med_name = st.text_input("Medicine Name")
    med_price = st.number_input("Price", min_value=0.0, step=0.1)
    med_quantity = st.number_input("Quantity", min_value=0, step=1)
    med_expiry = st.date_input("Expiry Date")
    
    add_medicine = st.form_submit_button("Add Medicine")
    
    if add_medicine:
        if med_name and med_price > 0 and med_quantity > 0:
            new_entry = pd.DataFrame([[med_id, med_name, med_price, med_quantity, med_expiry]],
                                     columns=df.columns)
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv("pharmacy_inventory.csv", index=False)
            st.success(f"✅ {med_name} added successfully!")
        else:
            st.markdown("<p class='error'>⚠️ Please fill all fields correctly!</p>", unsafe_allow_html=True)
