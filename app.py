import streamlit as st
import pandas as pd

# Load Pharmacy Data
pharmacy_file = "pharmacy.csv"

# Page Configuration
st.set_page_config(page_title="Pharmacy System", page_icon="🏥", layout="wide")

# Custom CSS for Professional Look
st.markdown("""
    <style>
        body { font-family: 'Arial', sans-serif; }
        .stApp { background-color: #1e1e2f; color: white; }
        .stDataFrame { background-color: white; color: black; }
        h1, h2, h3 { color: #ffcc00; }
        .success { background-color: #28a745; color: white; padding: 10px; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🏥 Pharmacy Management System")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv(pharmacy_file)

df = load_data()

# Sidebar Navigation
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2731/2731924.png", width=100)
st.sidebar.header("🔹 Navigation")
menu = st.sidebar.radio("Go to", ["📋 Inventory", "➕ Add Medicine"])

# View Inventory
if menu == "📋 Inventory":
    st.subheader("📋 View Medicine Inventory")
    st.dataframe(df)

    # Search Medicine
    search = st.text_input("🔍 Search Medicine by Name")
    if search:
        result = df[df["Name"].str.lower().str.contains(search.lower())]
        st.dataframe(result)

# Add Medicine
elif menu == "➕ Add Medicine":
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

