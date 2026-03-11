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

# --- BLOCK B: BUYER TICKET DISPLAY (TESTING VERSION) ---
if "ticket" in st.query_params:
    ticket_code = st.query_params["ticket"]
    
    # Setup clean mobile view
    st.set_page_config(initial_sidebar_state="collapsed")
    
    sales_df = conn.read(worksheet="Sales", ttl=0)
    match = sales_df[sales_df['Coupon Code'] == ticket_code]
    
    if not match.empty:
        buyer_name = match.iloc[0]['Buyer Name']
        buyer_mobile = match.iloc[0]['Mobile']
        
        # --- THE DIGITAL TICKET WIREFRAME ---
        with st.container(border=True):
            
            # SECTION 1: TOP BRANDING (PLACEHOLDERS)
            t_col1, t_col2 = st.columns([1, 4])
            with t_col1:
                st.markdown("### 🏵️")
                st.caption("[Logo Here]")
            with t_col2:
                st.markdown("<h4 style='margin:0; text-align:right;'>MUZIRIS JMI</h4>", unsafe_allow_html=True)
                st.markdown("<h5 style='margin:0; text-align:right;'>KERALA FESTIVAL 2026</h5>", unsafe_allow_html=True)
            
            st.divider()

            # SECTION 2: DYNAMIC TICKET DATA
            st.success(f"✅ **VALID TICKET**")
            st.markdown(f"<h2 style='text-align:center;'>No. {ticket_code}</h2>", unsafe_allow_html=True)
            st.markdown(f"**Name:** {buyer_name}")
            st.markdown(f"**Phone:** {buyer_mobile}")
            
            st.divider()
            
            # SECTION 3: PRIZE IMAGERY (PLACEHOLDERS)
            st.info("📱 🔊 🎧 **[Large Image of Prizes Will Go Here]**")
            st.markdown("<h3 style='text-align:center; color:#CC9900;'>LUCKY DRAW CONTEST</h3>", unsafe_allow_html=True)
            st.markdown("🏆 **1st Prize:** Brand New Smartphone")
            st.markdown("🏆 **2nd Prize:** Premium Bluetooth Speaker")
            st.markdown("🏆 **3rd Prize:** Noise-Canceling Headphones")
            
            st.divider()

            # SECTION 4: VERIFICATION & PRICE BADGE
            f_col1, f_col2 = st.columns([3, 1])
            with f_col1:
                st.caption("🎟️ Present this digital coupon at the gate.")
                st.caption("*Winners announced on 9th April 2026*")
            with f_col2:
                # Custom CSS for the round ₹100 Price Badge
                st.markdown("""
                <div style='background-color:#1E3A8A; color:white; border-radius:50%; 
                            width:60px; height:60px; display:flex; 
                            align-items:center; justify-content:center; font-size:18px;
                            font-weight:bold; margin:auto;'>
                    ₹100
                </div>
                """, unsafe_allow_html=True)

    else:
        st.error("❌ Invalid or missing ticket code.")
        
    st.stop()

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
                    
# Generate the custom URL for this exact buyer
                # (Replace the URL below with your actual Streamlit Cloud URL!)
                base_url = "https://fest-coupons-app-vgmddeqz6bbvaoflhz9tqx.streamlit.app/"
                ticket_url = f"{base_url}?ticket={code}"
                
                msg = f"Hi {buyer}, thanks for supporting! Click here to view your official digital entry pass for the fest: {ticket_url}"
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