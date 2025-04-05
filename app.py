import streamlit as st
import pandas as pd

st.set_page_config(page_title="Pharmacy Management System", layout="wide")

# Load CSV
@st.cache_data
def load_data():
    return pd.read_csv("pharmacy_inventory.csv")

df = load_data()

# Sidebar
st.sidebar.title("Pharmacy Menu")
option = st.sidebar.radio("Choose an action", ["📋 View Inventory", "🔍 Search Medicine", "➕ Add Medicine"])

st.title("💊 Pharmacy Management System")

if option == "📋 View Inventory":
    st.subheader("🧾 All Medicines")
    st.dataframe(df, use_container_width=True)

elif option == "🔍 Search Medicine":
    st.subheader("🔍 Search for a Medicine")
    name = st.text_input("Enter medicine name:")
    if name:
        result = df[df['Name'].str.contains(name, case=False)]
        if not result.empty:
            st.success(f"{len(result)} medicine(s) found:")
            st.dataframe(result, use_container_width=True)
        else:
            st.warning("⚠️ No medicine found.")

elif option == "➕ Add Medicine":
    st.subheader("➕ Add New Medicine")
    with st.form("add_medicine"):
        med_id = st.number_input("Medicine ID", min_value=1)
        name = st.text_input("Name")
        price = st.number_input("Price", min_value=0.0)
        quantity = st.number_input("Quantity", min_value=0)
        expiry = st.date_input("Expiry Date")
        submit = st.form_submit_button("Add Medicine")

        if submit:
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
