import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
import string
from datetime import datetime

# --- BLOCK A: SETUP ---
st.set_page_config(page_title="Fest Lucky Coupon", layout="centered")

# --- BLOCK B: BUYER TICKET DISPLAY (TESTING VERSION) ---
if "ticket" in st.query_params:
    ticket_code = st.query_params["ticket"]
    
    # Setup clean mobile view
    st.set_page_config(initial_sidebar_state="collapsed")
    
    # 1. HANDLE FESTIVAL COUPONS
    if ticket_code.startswith("FEST-"):
        sales_df = conn.read(worksheet="Sales", ttl=0)
        match = sales_df[sales_df['Coupon Code'] == ticket_code]
        
        if not match.empty:
            buyer_name = match.iloc[0]['Buyer Name']
            buyer_mobile = match.iloc[0]['Mobile']
            
            with st.container(border=True):
                # TOP BRANDING
                t_col1, t_col2 = st.columns([1, 4])
                with t_col1:
                    st.markdown("### 🏵️")
                    st.caption("[Logo Here]")
                with t_col2:
                    st.markdown("<h4 style='margin:0; text-align:right;'>MUZIRIS JMI</h4>", unsafe_allow_html=True)
                    st.markdown("<h5 style='margin:0; text-align:right;'>KERALA FESTIVAL 2026</h5>", unsafe_allow_html=True)
                
                st.divider()

                # DYNAMIC TICKET DATA
                st.success(f"✅ **VALID TICKET**")
                st.markdown(f"<h2 style='text-align:center;'>No. {ticket_code}</h2>", unsafe_allow_html=True)
                st.markdown(f"**Name:** {buyer_name}")
                st.markdown(f"**Phone:** {buyer_mobile}")
                
                st.divider()
                
                # PRIZE IMAGERY
                st.info("📱 🔊 🎧 **[Large Image of Prizes Will Go Here]**")
                st.markdown("<h3 style='text-align:center; color:#CC9900;'>LUCKY DRAW CONTEST</h3>", unsafe_allow_html=True)
                st.markdown("🏆 **1st Prize:** Brand New Smartphone")
                st.markdown("🏆 **2nd Prize:** Premium Bluetooth Speaker")
                st.markdown("🏆 **3rd Prize:** Noise-Canceling Headphones")
                
                st.divider()

                # VERIFICATION & PRICE BADGE
                f_col1, f_col2 = st.columns([3, 1])
                with f_col1:
                    st.caption("🎟️ Present this digital coupon at the gate.")
                    st.caption("*Winners announced on 9th April 2026*")
                with f_col2:
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

    # 2. HANDLE DONATION RECEIPTS
    elif ticket_code.startswith("DON-"):
        donations_df = conn.read(worksheet="Donations", ttl=0)
        match = donations_df[donations_df['Receipt Code'] == ticket_code]
        
        if not match.empty:
            donor_name = match.iloc[0]['Donor Name']
            amount = match.iloc[0]['Amount']
            
            with st.container(border=True):
                st.markdown("### 🏵️ MUZIRIS JMI KERALA FESTIVAL 2026")
                st.divider()
                st.success("✅ **Official Donation Receipt**")
                
                st.markdown(f"<h3 style='text-align:center; color:#1E3A8A;'>Receipt: {ticket_code}</h3>", unsafe_allow_html=True)
                st.markdown(f"**Donor Name:** {donor_name}")
                st.markdown(f"**Amount Contributed:** ₹{amount}")
                
                st.divider()
                st.info("🙏 Thank you for your generous support of the Malayali Committee!")
                
                # Here is the placeholder for your Gadget Sponsor's Link!
                st.divider()
                st.warning("🎁 **Exclusive Sponsor Offer:** Get 30% off smart gadgets at [Sponsor Name]! Use code JMIFEST30.")
                st.button("Claim 30% Off Now") 
        else:
            st.error("❌ Invalid or missing receipt code.")
            
    else:
        st.error("❌ Unrecognized link format.")
        
    st.stop()

# --- BLOCK C: REGISTRATION FORM ---
st.title("🎟️ Community Fundraiser")

# --- TABS FOR CLEAN UI ---
tab1, tab2, tab3 = st.tabs(["🎟️ Sell Coupon", "💸 Register Donation", "🏆 Leaderboard"])

# ==========================================
# TAB 1: THE LUCKY DRAW COUPON FORM
# ==========================================
with tab1:
    with st.form("coupon_form", clear_on_submit=True):
        st.subheader("Register a ₹100 Coupon Sale")
        seller_id = st.text_input("Your Student ID", placeholder="e.g., 1001", key="c_id")
        buyer = st.text_input("Buyer Name", key="c_name")
        mobile = st.text_input("Buyer Mobile (e.g., 9198...)", key="c_mobile")
        
        if st.form_submit_button("Register Coupon", type="primary"):
            if seller_id and buyer and mobile:
                clean_id = seller_id.strip()
                match = member_df[member_df['ID'].astype(str).str.split('.').str[0] == clean_id]
                
                if not match.empty:
                    seller_name = match.iloc[0]['Name']
                    full_seller_info = f"{seller_name} ({clean_id})"
                    code = "FEST-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                    
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
                    
                    st.success(f"✅ Coupon {code} registered by {seller_name}!")
                    
                    clean_mobile = mobile.replace(" ", "")
                    if len(clean_mobile) == 10: clean_mobile = "91" + clean_mobile
                    
                    # NOTE: Replace 'YOUR-EXACT-URL' before deploying!
                    ticket_url = f"https://fest-coupons-app-vgmddeqz6bbvaoflhz9tqx.streamlit.app/?ticket={code}"
                    msg = f"Hi {buyer}, thanks for entering the lucky draw! View your official digital coupon and our sponsor offers here: {ticket_url}"
                    st.link_button("📲 Send Coupon via WhatsApp", f"https://wa.me/{clean_mobile}?text={msg.replace(' ', '%20')}")
                else:
                    st.error("Student ID not found!")
            else:
                st.error("Please fill in all details.")

# ==========================================
# TAB 2: THE DONATION FORM
# ==========================================
with tab2:
    with st.form("donation_form", clear_on_submit=True):
        st.subheader("Register a Custom Donation")
        d_seller_id = st.text_input("Your Student ID", placeholder="e.g., 1001", key="d_id")
        donor = st.text_input("Donor Name", key="d_name")
        amount = st.number_input("Donation Amount (₹)", min_value=1, step=10, key="d_amount")
        d_mobile = st.text_input("Donor Mobile (Optional - Leave blank if they prefer)", key="d_mobile")
        
        if st.form_submit_button("Register Donation", type="primary"):
            if d_seller_id and donor and amount > 0:
                clean_id = d_seller_id.strip()
                match = member_df[member_df['ID'].astype(str).str.split('.').str[0] == clean_id]
                
                if not match.empty:
                    seller_name = match.iloc[0]['Name']
                    full_seller_info = f"{seller_name} ({clean_id})"
                    don_code = "DON-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                    
                    new_don_row = pd.DataFrame([{
                        "Timestamp": datetime.now().strftime("%d/%m %H:%M"),
                        "Student Info": full_seller_info,
                        "Donor Name": donor,
                        "Mobile": d_mobile,
                        "Amount": amount,
                        "Receipt Code": don_code
                    }])
                    
                    donations_df = conn.read(worksheet="Donations", ttl=0)
                    updated_dons = pd.concat([donations_df, new_don_row], ignore_index=True)
                    conn.update(worksheet="Donations", data=updated_dons)
                    
                    st.success(f"✅ ₹{amount} donation from {donor} logged by {seller_name}!")
                    
                    # Only show WhatsApp button if they provided a number
                    if d_mobile:
                        clean_mobile = d_mobile.replace(" ", "")
                        if len(clean_mobile) == 10: clean_mobile = "91" + clean_mobile
                        
                        receipt_url = f"https://fest-coupons-app-vgmddeqz6bbvaoflhz9tqx.streamlit.app/?ticket={don_code}"
                        msg = f"Hi {donor}, thank you for your generous donation of ₹{amount} to the JMI Malayali Fest. View your official receipt and sponsor offers here: {receipt_url}"
                        st.link_button("📲 Send Receipt via WhatsApp", f"https://wa.me/{clean_mobile}?text={msg.replace(' ', '%20')}")
                else:
                    st.error("Student ID not found!")
            else:
                st.error("Please enter Student ID, Donor Name, and Amount.")

# ==========================================
# TAB 3: THE AUTOMATED LEDGER & LEADERBOARD
# ==========================================
with tab3:
    st.subheader("Live Revenue Leaderboard")
    
    if st.button("🔄 Refresh Data"):
        # 1. Fetch live data
        sales_df = conn.read(worksheet="Sales", ttl=0)
        donations_df = conn.read(worksheet="Donations", ttl=0)
        
        # 2. Calculate Coupon Revenue (Count * ₹100)
        sales_summary = sales_df.groupby('Student Info').size().reset_index(name='Coupons Sold')
        sales_summary['Coupon Revenue'] = sales_summary['Coupons Sold'] * 100
        
        # 3. Calculate Donations (Sum of amounts)
        if not donations_df.empty:
            donations_df['Amount'] = pd.to_numeric(donations_df['Amount'], errors='coerce').fillna(0)
            donations_summary = donations_df.groupby('Student Info')['Amount'].sum().reset_index(name='Donations Collected')
        else:
            donations_summary = pd.DataFrame(columns=['Student Info', 'Donations Collected'])
            
        # 4. Merge them together to find TOTAL OWED
        ledger_df = pd.merge(sales_summary, donations_summary, on='Student Info', how='outer').fillna(0)
        ledger_df['Total Owed (₹)'] = ledger_df['Coupon Revenue'] + ledger_df['Donations Collected']
        
        # Format the numbers cleanly
        ledger_df['Coupons Sold'] = ledger_df['Coupons Sold'].astype(int)
        ledger_df['Donations Collected'] = ledger_df['Donations Collected'].astype(int)
        ledger_df['Total Owed (₹)'] = ledger_df['Total Owed (₹)'].astype(int)
        
        # Sort by who brought in the most money
        ledger_df = ledger_df.sort_values(by='Total Owed (₹)', ascending=False).reset_index(drop=True)
        
        # 5. Overwrite the Ledger tab in Google Sheets
        conn.update(worksheet="Ledger", data=ledger_df)
        
        # 6. Display it beautifully on screen!
        st.dataframe(ledger_df, use_container_width=True)