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
    # MOBILE FIX: Simple text input instead of a buggy dropdown
    seller_id = st.text_input("Your Student ID", placeholder="e.g., 1001")
    
    buyer = st.text_input("Buyer Name")
    mobile = st.text_input("Buyer Mobile (e.g., 9198...)")
    
    if st.form_submit_button("Register Sale"):
        if seller_id and buyer and mobile:
            
            # 1. Look up the seller's name from the Google Sheet
            clean_id = seller_id.strip()
            match = member_df[member_df['ID'].astype(str).str.split('.').str[0] == clean_id]
            
            if not match.empty:
                # We found the student!
                seller_name = match.iloc[0]['Name']
                full_seller_info = f"{seller_name} ({clean_id})"
                
                # 2. Generate the unique code
                code = "FEST-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                
                # 3. Format and save to Google Sheets
                new_row = pd.DataFrame([{
                    "Timestamp": datetime.now().strftime("%d/%m %H:%M"),
                    "Student Info": full_seller_info,
                    "Buyer Name": buyer,
                    "Mobile": mobile,
                    "Coupon Code": code
                }])
                
                sales_df = conn.read(worksheet="Sales", ttl=0)
                updated_sales = pd.concat([sales_df, new_row], ignore_index=True)
                conn.update(worksheet="Sales", data=updated_sales)
                
                st.success(f"Registered by {seller_name}! Coupon Code: {code}")
                
                # 4. WHATSAPP FIX: Automatically add '91' if it's a 10-digit number
                clean_mobile = mobile.replace(" ", "")
                if len(clean_mobile) == 10:
                    clean_mobile = "91" + clean_mobile
                    
                msg = f"Hi {buyer}, your lucky coupon code for the fest is {code}. Thanks for supporting!"
                st.link_button("📲 Send to Buyer", f"https://wa.me/{clean_mobile}?text={msg.replace(' ', '%20')}")
                
            else:
                # If they type the wrong ID, stop them and show an error
                st.error("Student ID not found! Please check your ID and try again.")
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