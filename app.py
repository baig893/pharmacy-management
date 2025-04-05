import streamlit as st
import pandas as pd
from datetime import datetime

# --------------- CSS Styling ---------------
st.markdown("""
    <style>
    .main-title {
        font-size: 3rem;
        color: #0099ff;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #0099ff;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #006bb3;
    }
    .reportview-container {
        background: #f0f2f6;
    }
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    .sidebar .sidebar-content {
        background-color: #e6f2ff;
    }
    </style>
""", unsafe_allow_html=True)

# --------------- Title --------------------
st.markdown("<div class='main-title'>💊 Pharmacy Inventory Management</div>", unsafe_allow_html=True)

# --------------- Load Data ----------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("pharmacy_inventory.csv")
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Medicine ID", "Name", "Price", "Quantity", "Expiry Date"])

df = load_data()

# --------------- Sidebar ------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2865/2865535.png", width=100)
st.sidebar.title("📋 Menu")
menu = st.sidebar.radio("Navigate", ["View Inventory", "Search Medicine", "Add Medicine", "Low Stock Report"])

# --------------- View Inventory ------------
if menu == "View Inventory":
    st.subheader("📦 Complete Medicine Inventory")
    if df.empty:
        st.warning("Inventory is empty. Please add some medicines.")
    else:
        st.dataframe(df, use_container_width=True)

# --------------- Search Medicine -----------
elif menu == "Search Medicine":
    st.subheader("🔍 Search for Medicine by Name")
    query = st.text_input("Enter Medicine Name")
    if query:
        results = df[df["Name"].str.contains(query, case=False)]
        if not results.empty:
            st.success(f"✅ Found {len(results)} result(s)")
            st.dataframe(results, use_container_width=True)
        else:
            st.error("❌ No matching medicine found.")

# --------------- Add Medicine --------------
elif menu == "Add Medicine":
    st.subheader("➕ Add New Medicine to Inventory")
    with st.form("add_medicine_form"):
        med_id = st.number_input("Medicine ID", min_value=1)
        name = st.text_input("Medicine Name")
        price = st.number_input("Price (PKR)", min_value=0.0)
        quantity = st.number_input("Quantity", min_value=0)
        expiry = st.date_input("Expiry Date")
        submitted = st.form_submit_button("Add Medicine")

        if submitted:
            new_row = {
                "Medicine ID": med_id,
                "Name": name,
                "Price": price,
                "Quantity": quantity,
                "Expiry Date": expiry.strftime("%Y-%m-%d")
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv("pharmacy_inventory.csv", index=False)
            st.success("✅ Medicine added successfully!")

# --------------- Low Stock Report ----------
elif menu == "Low Stock Report":
    st.subheader("📉 Low Stock Report (Quantity < 10)")
    low_stock = df[df["Quantity"] < 10]
    if not low_stock.empty:
        st.warning("⚠️ Some medicines are low on stock!")
        st.dataframe(low_stock, use_container_width=True)
    else:
        st.success("✅ All medicines are sufficiently stocked.")

# --------------- Footer --------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>Made by <b>Abdul Rahman Baig</b> | © 2025</p>",
    unsafe_allow_html=True
)
