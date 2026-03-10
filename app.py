import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
import string
from datetime import datetime

# --- BLOCK A: SETUP ---
st.set_page_config(page_title="Fest Lucky Coupon", layout="centered")

# --- BLOCK B: CONNECT TO GOOGLE SHEETS ---
# This connects using your secrets.toml file
conn = st.connection("gsheets", type=GSheetsConnection)

# Read the "Members" tab to populate the dropdown menu
member_df = conn.read(worksheet="Members")
member_options = member_df['Name'] + " (" + member_df['ID'].astype(str) + ")"

# --- BLOCK C: REGISTRATION FORM ---
st.title("🎟️ Community Fundraiser")

with st.form("main_form", clear_on_submit=True):
    # UX FIX: Added index=None and a placeholder so it acts like a true search bar
    seller = st.selectbox(
        "Select Your Name & ID", 
        options=member_options,
        index=None,
        placeholder="🔍 Click here and type to search..."
    )
    
    buyer = st.text_input("Buyer Name")
    mobile = st.text_input("Buyer Mobile (e.g., 9198...)")
    
    if st.form_submit_button("Register Sale"):
        if seller and buyer and mobile:
            code = "FEST-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            
            new_row = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%d/%m %H:%M"),
                "Student Info": seller,
                "Buyer Name": buyer,
                "Mobile": mobile,
                "Coupon Code": code
            }])
            
            # CACHE FIX: Added ttl=0 so it reads fresh data from Google every single time
            sales_df = conn.read(worksheet="Sales", ttl=0)
            updated_sales = pd.concat([sales_df, new_row], ignore_index=True)
            conn.update(worksheet="Sales", data=updated_sales)
            
            st.success(f"Registered! Coupon Code: {code}")
            
            msg = f"Hi {buyer}, your lucky coupon code for the fest is {code}. Thanks for supporting!"
            st.link_button("📲 Send to Buyer", f"https://wa.me/{mobile}?text={msg.replace(' ', '%20')}")
        else:
            st.error("Please fill in all details.")

# --- BLOCK D: LIVE LEADERBOARD ---
st.divider()
st.header("🏆 Trip Leaderboard")

# CACHE FIX: Added ttl=0 so the leaderboard updates instantly
all_sales = conn.read(worksheet="Sales", ttl=0)

# We use dropna() to ignore any completely blank rows Google Sheets might have added
if not all_sales.dropna(how='all').empty:
    counts = all_sales['Student Info'].value_counts().reset_index()
    counts.columns = ['Student', 'Sold']
    st.table(counts.head(10))