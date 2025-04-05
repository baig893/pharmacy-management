import streamlit as st
import pandas as pd
from datetime import datetime

# ----------------- Custom CSS -----------------
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #e0f7fa, #e1bee7);
    }
    .main-title {
        font-size: 3rem;
        color: #4a148c;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 10px #c2185b66;
    }

    .sidebar .sidebar-content {
        background-color: #f3e5f5;
        padding: 1.5rem;
        border-radius: 0 20px 20px 0;
        font-family: 'Segoe UI', sans-serif;
        border-right: 6px solid #8e24aa;
        box-shadow: 4px 0 15px #ab47bc33;
    }

    .css-1aumxhk {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        transition: 0.3s;
    }

    .css-1aumxhk:hover {
        background-color: #fce4ec;
        box-shadow: 0 0 20px #f0629222;
        transform: scale(1.03);
    }

    .stButton>button {
        background: linear-gradient(to right, #8e24aa, #d81b60);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.4rem;
        transition: all 0.3s ease-in-out;
    }

    .stButton>button:hover {
        background-color: #ad1457;
        box-shadow: 0 0 10px #ff4081aa;
    }

    .stDataFrame {
        border-radius: 16px;
        overflow: hidden;
        background: #fff;
        box-shadow: 0 0 16px #e1bee7aa;
    }

    .search-animation {
        font-size: 60px;
        text-align: center;
        margin-bottom: 1rem;
    }

    .footer {
        text-align: center;
        font-size: 14px;
        color: #6a1b9a;
        margin-top: 3rem;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- Title ---------------------
st.markdown("<div class='main-title'>💊 Smart Pharmacy Inventory System</div>", unsafe_allow_html=True)

# ----------------- Load Inventory ----------------
@st.cache_data

def load_data():
    try:
        return pd.read_csv("pharmacy_inventory.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Medicine ID", "Name", "Price", "Quantity", "Expiry Date"])

df = load_data()

# ----------------- Sidebar Menu ------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2906/2906277.png", width=100)
st.sidebar.markdown("## 📋 <u>Main Menu</u>", unsafe_allow_html=True)

menu = st.sidebar.radio("Choose an option", [
    "📦 View Inventory",
    "🔍 Search Medicine",
    "➕ Add Medicine",
    "⚠️ Low Stock Report"
])

# ----------------- View Inventory ------------------
if menu == "📦 View Inventory":
    st.subheader("📋 Complete Medicine Inventory")
    if df.empty:
        st.warning("Inventory is empty. Please add medicines.")
    else:
        st.dataframe(df, use_container_width=True)

# ----------------- Search Medicine ------------------
elif menu == "🔍 Search Medicine":
    st.subheader("🔬 Find a Medicine")
    st.markdown("<div class='search-animation'>🧪🔎</div>", unsafe_allow_html=True)

    query = st.text_input("Enter Medicine Name").strip()

    if query:
        results = df[df["Name"].str.contains(query, case=False)]
        if not results.empty:
            st.success(f"✅ Found {len(results)} result(s).")
            st.dataframe(results, use_container_width=True)
            st.markdown("🎯 Your medicine is in stock. Stay safe!")
        else:
            st.error("❌ No such medicine found.")
            st.markdown("🧭 Try adding this to inventory.")

# ----------------- Add Medicine ------------------
elif menu == "➕ Add Medicine":
    st.subheader("➕ Add New Medicine to Inventory")

    with st.form("add_form"):
        med_id = st.number_input("Medicine ID", min_value=1)
        name = st.text_input("Medicine Name")
        price = st.number_input("Price (PKR)", min_value=0.0)
        quantity = st.number_input("Quantity", min_value=0)
        expiry = st.date_input("Expiry Date")
        add = st.form_submit_button("Add Medicine")

        if add:
            new_row = {
                "Medicine ID": med_id,
                "Name": name,
                "Price": price,
                "Quantity": quantity,
                "Expiry Date": expiry.strftime("%Y-%m-%d")
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv("pharmacy_inventory.csv", index=False)
            st.success("✅ New medicine added successfully!")

# ----------------- Low Stock Report ------------------
elif menu == "⚠️ Low Stock Report":
    st.subheader("🚨 Low Stock Alerts")
    low_stock = df[df["Quantity"] < 10]
    if not low_stock.empty:
        st.warning("These medicines are running low:")
        st.dataframe(low_stock, use_container_width=True)
    else:
        st.success("🎉 All medicines are sufficiently stocked.")

# ----------------- Footer ------------------
st.markdown("""
    <div class='footer'>
    🚀 Created with ❤️ by <strong> BUSHRA </strong> | 2025 | 
""", unsafe_allow_html=True)
