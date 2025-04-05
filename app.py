import streamlit as st
import pandas as pd
from datetime import datetime

# ----------------- Custom CSS -----------------
st.markdown("""
    <style>
    /* Global app style */
    body {
        background-color: #f5f7fa;
    }
    .main-title {
        font-size: 3rem;
        color: #0d6efd;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 8px #aaa;
    }

    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: #e0f0ff;
        padding: 1.5rem;
        border-right: 4px solid #00aaff;
        border-radius: 0 20px 20px 0;
        font-family: 'Segoe UI', sans-serif;
    }

    .css-1aumxhk {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        transition: 0.3s;
    }

    .css-1aumxhk:hover {
        background-color: #d9f1ff;
        box-shadow: 0 0 15px #00c3ff60;
        transform: scale(1.03);
    }

    .stButton>button {
        background-color: #00aaff;
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease-in-out;
    }

    .stButton>button:hover {
        background-color: #0077cc;
    }

    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        background: #fff;
        box-shadow: 0 0 12px #ccc;
    }

    .search-animation {
        font-size: 50px;
        text-align: center;
        margin-bottom: 1rem;
    }

    </style>
""", unsafe_allow_html=True)

# ----------------- Title ---------------------
st.markdown("<div class='main-title'>💊 Pharmacy Inventory Management</div>", unsafe_allow_html=True)

# ----------------- Load Inventory ----------------
@st.cache_data
def load_data():
    try:
        return pd.read_csv("pharmacy_inventory.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Medicine ID", "Name", "Price", "Quantity", "Expiry Date"])

df = load_data()

# ----------------- Sidebar Menu ------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2906/2906277.png", width=90)
st.sidebar.markdown("## 📋 <u>Menu</u>", unsafe_allow_html=True)

menu = st.sidebar.radio("Navigate", [
    "🧾 View Inventory",
    "🔍 Search Medicine",
    "➕ Add Medicine",
    "⚠️ Low Stock Report"
])

# ----------------- View Inventory ------------------
if menu == "🧾 View Inventory":
    st.subheader("📦 Current Medicine Inventory")
    if df.empty:
        st.warning("No data found. Please add some medicines.")
    else:
        st.dataframe(df, use_container_width=True)

# ----------------- Search Medicine ------------------
elif menu == "🔍 Search Medicine":
    st.subheader("🔍 Search for a Medicine")

    st.markdown("<div class='search-animation'>🧬🔎</div>", unsafe_allow_html=True)

    query = st.text_input("Enter Medicine Name").strip()

    if query:
        results = df[df["Name"].str.contains(query, case=False)]
        if not results.empty:
            st.success(f"✅ {len(results)} result(s) found.")
            st.dataframe(results, use_container_width=True)
            st.markdown("🎉 Medicine is available! Stay healthy 💪")
        else:
            st.error("❌ No matching medicine found.")
            st.markdown("😕 Try checking the spelling or add this medicine to inventory.")

# ----------------- Add Medicine ------------------
elif menu == "➕ Add Medicine":
    st.subheader("➕ Add New Medicine")

    with st.form("add_form"):
        med_id = st.number_input("Medicine ID", min_value=1)
        name = st.text_input("Medicine Name")
        price = st.number_input("Price (PKR)", min_value=0.0)
        quantity = st.number_input("Quantity", min_value=0)
        expiry = st.date_input("Expiry Date")
        add = st.form_submit_button("Add")

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
            st.success("✅ Medicine added successfully!")

# ----------------- Low Stock ------------------
elif menu == "⚠️ Low Stock Report":
    st.subheader("📉 Low Stock Alert (Qty < 10)")
    low_stock = df[df["Quantity"] < 10]
    if not low_stock.empty:
        st.warning("⚠️ Some medicines are running low!")
        st.dataframe(low_stock, use_container_width=True)
    else:
        st.success("✅ All stock levels are healthy.")

# ----------------- Footer ------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; font-size:14px;'>🚀 Made by <b>Abdul Rahman Baig</b> | 2025 | Powered by Streamlit</p>",
    unsafe_allow_html=True
)
