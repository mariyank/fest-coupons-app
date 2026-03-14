import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
import string
import base64
import os
from datetime import datetime

# --- BLOCK A: SETUP ---
st.set_page_config(page_title="Muziris '26", page_icon="🎪", layout="centered", initial_sidebar_state="collapsed")

# --- DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)
# We only load members initially. Sales and Donations load on demand to speed up the app.
member_df = conn.read(worksheet="Members", ttl=0)

# --- HELPER: LOAD IMAGES FOR HTML ---
def load_image_base64(img_name):
    if os.path.exists(img_name):
        with open(img_name, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            ext = "png" if img_name.lower().endswith(".png") else "jpeg"
            return f"data:image/{ext};base64,{encoded}"
    return ""

myg_url = "https://www.myg.in/?srsltid=AfmBOooV4bFo8kgYX1cuhrlgiSD6BEnIImreRGal6opfUojOJ2mJ0XP8"

# =====================================================================
# BLOCK B: PREMIUM TICKET DISPLAY (THE "EARLY EXIT" FLATTENING)
# =====================================================================
if "ticket" in st.query_params:
    ticket_code = st.query_params["ticket"]
    
    img_smrti = load_image_base64("smrti.png")
    img_muziris = load_image_base64("muziris.png")
    img_myg = load_image_base64("myg.png")
    img_title = load_image_base64("title.png")
    img_donation = load_image_base64("donation.png")

    m_base = "-webkit-mask-image: radial-gradient(circle at 0 0, transparent 16px, black 16.5px), radial-gradient(circle at 100% 0, transparent 16px, black 16.5px), radial-gradient(circle at 0 100%, transparent 16px, black 16.5px), radial-gradient(circle at 100% 100%, transparent 16px, black 16.5px); -webkit-mask-position: top left, top right, bottom left, bottom right; -webkit-mask-size: 51% 51%; -webkit-mask-repeat: no-repeat;"
    m_border = "-webkit-mask-image: radial-gradient(circle at 0 0, transparent 22px, black 22.5px), radial-gradient(circle at 100% 0, transparent 22px, black 22.5px), radial-gradient(circle at 0 100%, transparent 22px, black 22.5px), radial-gradient(circle at 100% 100%, transparent 22px, black 22.5px); -webkit-mask-position: top left, top right, bottom left, bottom right; -webkit-mask-size: 51% 51%; -webkit-mask-repeat: no-repeat;"
    m_inner = "-webkit-mask-image: radial-gradient(circle at 0 0, transparent 28px, black 28.5px), radial-gradient(circle at 100% 0, transparent 28px, black 28.5px), radial-gradient(circle at 0 100%, transparent 28px, black 28.5px), radial-gradient(circle at 100% 100%, transparent 28px, black 28.5px); -webkit-mask-position: top left, top right, bottom left, bottom right; -webkit-mask-size: 51% 51%; -webkit-mask-repeat: no-repeat;"
    
    mt_base = "-webkit-mask-image: radial-gradient(circle at 0 0, transparent 8px, black 8.5px), radial-gradient(circle at 100% 0, transparent 8px, black 8.5px), radial-gradient(circle at 0 100%, transparent 8px, black 8.5px), radial-gradient(circle at 100% 100%, transparent 8px, black 8.5px); -webkit-mask-position: top left, top right, bottom left, bottom right; -webkit-mask-size: 51% 51%; -webkit-mask-repeat: no-repeat;"
    mt_border = "-webkit-mask-image: radial-gradient(circle at 0 0, transparent 10px, black 10.5px), radial-gradient(circle at 100% 0, transparent 10px, black 10.5px), radial-gradient(circle at 0 100%, transparent 10px, black 10.5px), radial-gradient(circle at 100% 100%, transparent 10px, black 10.5px); -webkit-mask-position: top left, top right, bottom left, bottom right; -webkit-mask-size: 51% 51%; -webkit-mask-repeat: no-repeat;"
    mt_inner = "-webkit-mask-image: radial-gradient(circle at 0 0, transparent 12px, black 12.5px), radial-gradient(circle at 100% 0, transparent 12px, black 12.5px), radial-gradient(circle at 0 100%, transparent 12px, black 12.5px), radial-gradient(circle at 100% 100%, transparent 12px, black 12.5px); -webkit-mask-position: top left, top right, bottom left, bottom right; -webkit-mask-size: 51% 51%; -webkit-mask-repeat: no-repeat;"

    # --- 1. HANDLE FESTIVAL COUPONS ---
    if ticket_code.startswith("FEST-"):
        sales_df = conn.read(worksheet="Sales", ttl=0)
        match = sales_df[sales_df['Coupon Code'] == ticket_code]
        
        if not match.empty:
            buyer_name = match.iloc[0]['Buyer Name']
            buyer_mobile = match.iloc[0]['Mobile']
            img_luckydraw = load_image_base64("luckydraw.png")
            img_prizes = load_image_base64("prizes.png")

            ticket_html = f"""
            <link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Aref+Ruqaa:wght@400;700&display=swap" rel="stylesheet">
            <div style="filter: drop-shadow(0px 8px 15px rgba(0,0,0,0.3)); max-width: 420px; margin: auto; font-family: 'Arial', sans-serif;">
            <div style="position: relative;">
            <div style="position: absolute; top:0; left:0; right:0; bottom:0; background-color: #FFF9E6; {m_base} z-index: 1;"></div>
            <div style="position: absolute; top:0; left:0; right:0; bottom:0; background-color: #E32636; border: 6px solid transparent; background-clip: padding-box; {m_border} z-index: 2;"></div>
            <div style="position: absolute; top:0; left:0; right:0; bottom:0; background-color: #FFF9E6; border: 12px solid transparent; background-clip: padding-box; {m_inner} z-index: 3;"></div>
            
            <div style="position: relative; z-index: 4; padding: 26px 26px 15px 26px; text-align: center;">
            <div style="padding-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; gap: 5px;"><img src="{img_smrti}" style="height:42px;"><img src="{img_muziris}" style="height:42px;"></div>
            <div style="flex-grow:1; display:flex; justify-content:center; align-items:center; padding: 0 5px;">
                <img src="{img_title}" style="max-height:36px; max-width:100%; object-fit:contain; padding: 0 8px;">
            </div>
            <img src="{img_myg}" style="height:32px; background:white; padding:4px; border-radius:4px; border:1px solid #E32636;">
            </div>
            
            <img src="{img_luckydraw}" style="width:240px; margin-bottom:15px;">
            
            <div style="margin: 0 auto 20px auto; position: relative; display: inline-block;">
            <div style="position: absolute; top:0; left:0; right:0; bottom:0; background-color: #088F8F; {mt_base} z-index: 1;"></div>
            <div style="position: absolute; top:0; left:0; right:0; bottom:0; background-color: #8F0808; border: 2px solid transparent; background-clip: padding-box; {mt_border} z-index: 2;"></div>
            <div style="position: absolute; top:0; left:0; right:0; bottom:0; background-color: #088F8F; border: 4px solid transparent; background-clip: padding-box; {mt_inner} z-index: 3;"></div>
            <div style="position: relative; z-index: 4; padding: 8px 20px; color: white; font-size: 18px; font-weight: bold;">No. {ticket_code}</div>
            </div>

            <div style="margin-bottom: 20px;">
                <div style="display:flex; justify-content:center; align-items:center; gap:8px; margin: 4px 0;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#222" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg><span style="font-size:26px; font-family:'Aref Ruqaa', serif; color: #222; margin-top: -4px;">{buyer_name}</span></div>
                <div style="display:flex; justify-content:center; align-items:center; gap:8px; margin: 4px 0;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#222" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg><span style="font-size:20px; font-family:'Amiri', serif; color: #222;">{buyer_mobile}</span></div>
            </div>

            <div><img src="{img_prizes}" style="width:100%; border-radius:8px; border:1px solid rgba(227,38,54,0.2);"></div>
            <p style="font-size:13px; color:#666; margin-top:10px;">🎟️ Present this digital pass at the entry gate.</p>
            </div></div>
            <div style="text-align:center; color:#E32636; font-size:18px; margin:-14px 0; position:relative; z-index:10; letter-spacing:4px;">✂ - - - - - - - - - -</div>
            <div style="background-color:#E32636; {m_base} padding:20px; text-align:center; position:relative;">
            <p style="color:#FFF9E6; font-size:12px; text-transform:uppercase; font-weight:bold; margin:0 0 8px 0;">Exclusive Sponsor Offer</p>
            <a href="{myg_url}" target="_blank" style="text-decoration:none; display:block;">
                <img src="{img_myg}" style="height:40px; background:white; padding:5px; border-radius:5px; margin-bottom:10px; display:inline-block;">
                <div style="background:#FF6600; color:white; padding:10px; border-radius:8px; border:2px dashed white; font-weight:bold; cursor:pointer;">🎁 Use code JMIFEST5 for 5% OFF!</div>
            </a>
            </div></div>
            """
            st.markdown(ticket_html, unsafe_allow_html=True)
        else:
            st.error("❌ Invalid or missing ticket code.")

    # --- 2. HANDLE DONATION RECEIPTS ---
    elif ticket_code.startswith("DON-"):
        donations_df = conn.read(worksheet="Donations", ttl=0)
        match = donations_df[donations_df['Receipt Code'] == ticket_code]
        
        if not match.empty:
            donor_name = match.iloc[0]['Donor Name']
            amount = match.iloc[0]['Amount']
            
            receipt_html = f"""
            <link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Aref+Ruqaa:wght@400;700&display=swap" rel="stylesheet">
            <div style="filter: drop-shadow(0px 8px 15px rgba(0,0,0,0.3)); max-width: 420px; margin: auto; font-family: 'Arial', sans-serif;">
            <div style="position: relative;">
            <div style="position: absolute; top:0; left:0; right:0; bottom:0; background-color: #FFF9E6; {m_base} z-index: 1;"></div>
            <div style="position: absolute; top:0; left:0; right:0; bottom:0; background-color: #E32636; border: 6px solid transparent; background-clip: padding-box; {m_border} z-index: 2;"></div>
            <div style="position: absolute; top:0; left:0; right:0; bottom:0; background-color: #FFF9E6; border: 12px solid transparent; background-clip: padding-box; {m_inner} z-index: 3;"></div>
            
            <div style="position: relative; z-index: 4; padding: 26px 26px 25px 26px; text-align: center;">
            <div style="padding-bottom: 15px; display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; gap: 5px;"><img src="{img_smrti}" style="height:42px;"><img src="{img_muziris}" style="height:42px;"></div>
            <div style="flex-grow:1; display:flex; justify-content:center; align-items:center; padding: 0 5px;">
                <img src="{img_title}" style="max-height:36px; max-width:100%; object-fit:contain; padding: 0 8px;">
            </div>
            <img src="{img_myg}" style="height:32px; background:white; padding:4px; border-radius:4px; border:1px solid #E32636;">
            </div>
            
            <div style="margin: 5px 0 15px 0;"><img src="{img_donation}" style="width: 240px; object-fit: contain;"></div>
            
            <div style="margin: 0 auto 25px auto; position: relative; display: inline-block;">
            <div style="position: absolute; top:0; left:0; right:0; bottom:0; background-color: #088F8F; {mt_base} z-index: 1;"></div>
            <div style="position: absolute; top:0; left:0; right:0; bottom:0; background-color: #8F0808; border: 2px solid transparent; background-clip: padding-box; {mt_border} z-index: 2;"></div>
            <div style="position: absolute; top:0; left:0; right:0; bottom:0; background-color: #088F8F; border: 4px solid transparent; background-clip: padding-box; {mt_inner} z-index: 3;"></div>
            <div style="position: relative; z-index: 4; padding: 8px 20px; color: white; font-size: 18px; font-weight: bold;">{ticket_code}</div>
            </div>

            <div style="margin-bottom: 10px;">
                <div style="display:flex; justify-content:center; align-items:center; gap:8px; margin: 4px 0;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#222" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg><span style="font-size:26px; font-family:'Aref Ruqaa', serif; color: #222; margin-top: -4px;">{donor_name}</span></div>
                <div style="display:flex; justify-content:center; align-items:center; gap:8px; margin: 4px 0;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#222" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg><span style="font-size:22px; font-family:'Amiri', serif; color: #222;">₹{amount}</span></div>
            </div>

            <hr style="border-top: 2px dashed rgba(227,38,54,0.4); margin:25px 10px 15px 10px;">
            <p style="font-size:16px; color:#222; margin-top:10px; font-weight:bold;">🙏 Thank you for your generous support!</p>
            </div></div>
            <div style="text-align:center; color:#E32636; font-size:18px; margin:-14px 0; position:relative; z-index:10; letter-spacing:4px;">✂ - - - - - - - - - -</div>
            <div style="background-color:#E32636; {m_base} padding:20px; text-align:center; position:relative;">
            <p style="color:#FFF9E6; font-size:12px; text-transform:uppercase; font-weight:bold; margin:0 0 8px 0;">Exclusive Sponsor Offer</p>
            <a href="{myg_url}" target="_blank" style="text-decoration:none; display:block;">
                <img src="{img_myg}" style="height:40px; background:white; padding:5px; border-radius:5px; margin-bottom:10px; display:inline-block;">
                <div style="background:#FF6600; color:white; padding:10px; border-radius:8px; border:2px dashed white; font-weight:bold; cursor:pointer;">🎁 Use code JMIFEST5 for 5% OFF!</div>
            </a>
            </div></div>
            """
            st.markdown(receipt_html, unsafe_allow_html=True)
        else:
            st.error("❌ Invalid or missing receipt code.")
    else:
        st.error("❌ Unrecognized link format.")
        
    # CRITICAL: Early exit! This flattens the rest of the file.
    st.stop()


# =====================================================================
# BLOCK C: ADMIN DASHBOARD (FLATTENED!)
# =====================================================================

# --- STYLISH VINTAGE HEADER ---
img_muziris = load_image_base64("muziris.png")
header_html = f"""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&display=swap" rel="stylesheet">
<div style="text-align: center; margin-bottom: 25px;">
    <h1 style="color: #E32636; font-family: 'Playfair Display', serif; font-weight: 700; display: flex; justify-content: center; align-items: center; gap: 15px; margin-bottom: 5px; font-size: 36px;">
        <img src="{img_muziris}" style="height: 50px; object-fit: contain;">
        Muziris '26 Admin
    </h1>
    <p style="color: #666; font-size: 16px; margin-top: 0;">Official Ticketing & Donation Dashboard</p>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["🎟️ Sell", "💸 Donate", "🏆 Leaderboard"])

# --- TAB 1: SELL COUPON ---
with tab1:
    with st.container(border=True):
        st.markdown("### 📝 New Lucky Draw Entry")
        with st.form("coupon_form", clear_on_submit=True):
            seller_id = st.text_input("👤 Your Student ID", placeholder="e.g., 1001", key="c_id")
            buyer = st.text_input("🗣️ Buyer Name", key="c_name", placeholder="Full Name")
            mobile = st.text_input("📱 Buyer Mobile", key="c_mobile", placeholder="10-digit number")
            
            if st.form_submit_button("💳 Generate ₹100 Coupon", type="primary", use_container_width=True):
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
                        st.error("❌ Student ID not found!")
                else:
                    st.warning("⚠️ Please fill in all details.")

# --- TAB 2: DONATION ---
with tab2:
    with st.container(border=True):
        st.markdown("### 🤝 Register a Donation")
        with st.form("donation_form", clear_on_submit=True):
            d_seller_id = st.text_input("👤 Your Student ID", placeholder="e.g., 1001", key="d_id")
            donor = st.text_input("🗣️ Donor Name", key="d_name", placeholder="Full Name or 'Anonymous'")
            amount = st.number_input("💵 Amount (₹)", min_value=10, step=50, value=500, key="d_amount")
            d_mobile = st.text_input("📱 Donor Mobile (Optional)", key="d_mobile", placeholder="For digital receipt")
            
            if st.form_submit_button("📜 Generate Receipt", type="primary", use_container_width=True):
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
                        
                        if d_mobile:
                            clean_mobile = d_mobile.replace(" ", "")
                            if len(clean_mobile) == 10: clean_mobile = "91" + clean_mobile
                            receipt_url = f"https://fest-coupons-app-vgmddeqz6bbvaoflhz9tqx.streamlit.app/?ticket={don_code}"
                            msg = f"Hi {donor}, thank you for your generous donation of ₹{amount} to the JMI Malayali Fest. View your official receipt and sponsor offers here: {receipt_url}"
                            st.link_button("📲 Send Receipt via WhatsApp", f"https://wa.me/{clean_mobile}?text={msg.replace(' ', '%20')}")
                    else:
                        st.error("❌ Student ID not found!")
                else:
                    st.warning("⚠️ Please enter Student ID, Donor Name, and Amount.")

# --- TAB 3: THE LIVE MOBILE-FIRST LEADERBOARD ---
with tab3:
    st.markdown("<h3 style='text-align: center; color: #E32636;'>🔥 Top Fundraisers 🔥</h3>", unsafe_allow_html=True)
    
    # 1. Fetch button loads data into session_state so it doesn't disappear when searching!
    if st.button("🔄 Load / Refresh Live Data", type="primary", use_container_width=True):
        with st.spinner("Crunching the latest numbers..."):
            sales_df = conn.read(worksheet="Sales", ttl=0)
            donations_df = conn.read(worksheet="Donations", ttl=0)
            
            # Summarize Sales & Find Latest Sale Time
            if not sales_df.empty:
                sales_summary = sales_df.groupby('Student Info').size().reset_index(name='Coupons')
                sales_df['ParsedTime'] = pd.to_datetime(sales_df['Timestamp'], format="%d/%m %H:%M", errors='coerce')
                sales_time = sales_df.groupby('Student Info')['ParsedTime'].max().reset_index(name='LastSale')
                sales_summary = pd.merge(sales_summary, sales_time, on='Student Info')
            else:
                sales_summary = pd.DataFrame(columns=['Student Info', 'Coupons', 'LastSale'])
                
            # Summarize Donations & Find Latest Donation Time
            if not donations_df.empty:
                donations_df['Amount'] = pd.to_numeric(donations_df['Amount'], errors='coerce').fillna(0)
                donations_summary = donations_df.groupby('Student Info')['Amount'].sum().reset_index(name='Donations')
                donations_df['ParsedTime'] = pd.to_datetime(donations_df['Timestamp'], format="%d/%m %H:%M", errors='coerce')
                don_time = donations_df.groupby('Student Info')['ParsedTime'].max().reset_index(name='LastDon')
                donations_summary = pd.merge(donations_summary, don_time, on='Student Info')
            else:
                donations_summary = pd.DataFrame(columns=['Student Info', 'Donations', 'LastDon'])
                
            # Merge both DataFrames (Without the global fillna!)
            ledger_df = pd.merge(sales_summary, donations_summary, on='Student Info', how='outer')
            
            # ONLY fill the number columns with 0, leaving missing timestamps alone
            ledger_df['Coupons'] = ledger_df['Coupons'].fillna(0).astype(int)
            ledger_df['Donations'] = ledger_df['Donations'].fillna(0).astype(int)
            ledger_df['Total (₹)'] = (ledger_df['Coupons'] * 100) + ledger_df['Donations']
            
            # Resolve the final Tie-Breaker "Last Active" timestamp safely
            ledger_df['Last Active'] = ledger_df[['LastSale', 'LastDon']].max(axis=1)
            
            # Sort by Highest Total, then Latest Active Time
            ledger_df = ledger_df.sort_values(by=['Total (₹)', 'Last Active'], ascending=[False, False]).reset_index(drop=True)
            
            # Clean up the final format for display
            ledger_df.rename(columns={'Student Info': 'Student Name'}, inplace=True)
            
            # Save to Google Sheets (without the raw datetime objects)
            clean_upload_df = ledger_df[['Student Name', 'Coupons', 'Donations', 'Total (₹)']]
            conn.update(worksheet="Ledger", data=clean_upload_df)
            
            # Save to Session State for the UI
            st.session_state['live_leaderboard'] = ledger_df

    # 2. Render UI if data exists in session state
    if 'live_leaderboard' in st.session_state and not st.session_state['live_leaderboard'].empty:
        df = st.session_state['live_leaderboard']
        
        # --- FIRE PROGRESS BAR (0 to 2000) ---
        TOTAL_TARGET = 2000
        current_sold = df['Coupons'].sum()
        percentage = min((current_sold / TOTAL_TARGET) * 100, 100)
        
        progress_html = f"""
        <style>
        @keyframes glow {{
          0% {{ box-shadow: 0 0 5px #ff4500, 0 0 10px #ff4500; }}
          100% {{ box-shadow: 0 0 15px #ff8c00, 0 0 20px #ffd700; }}
        }}
        </style>
        <div style="margin-bottom: 25px; margin-top: 15px;">
            <p style="text-align: center; font-weight: bold; color: #444; margin-bottom: 5px;">Festival Goal: {current_sold} / {TOTAL_TARGET} Coupons Sold ✨</p>
            <div style="width: 100%; background-color: #e0e0e0; border-radius: 15px; height: 25px; overflow: hidden; border: 1px solid #ccc;">
                <div style="width: {percentage}%; height: 100%; background: linear-gradient(90deg, #ff0000, #ff8c00, #ffcc00); border-radius: 15px; text-align: right; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px; animation: glow 1.5s infinite alternate;">
                    <span style="font-size: 16px;">🔥</span>
                </div>
            </div>
        </div>
        """
        st.markdown(progress_html, unsafe_allow_html=True)
        st.divider()

        # --- METALLIC PODIUM CARDS ---
        def make_podium_card(bg_gradient, border_color, text_dark, text_light, emoji, title, name, total, coupons, donations):
            return f"""
            <div style="background: {bg_gradient}; padding: 15px; border-radius: 10px; margin-bottom: 15px; border: 1px solid {border_color}; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h4 style="margin: 0; color: {text_dark}; font-size: 18px; font-family: sans-serif;">{emoji} {title} • {name}</h4>
                <h2 style="margin: 5px 0; color: {text_dark}; font-size: 32px; font-family: sans-serif; font-weight: bold;">₹{total}</h2>
                <p style="margin: 0; color: {text_light}; font-size: 14px; font-family: sans-serif; font-weight: bold;">{coupons} Coupons | ₹{donations} Donations</p>
            </div>
            """

        if len(df) > 0: st.markdown(make_podium_card("linear-gradient(135deg, #FFF9D6, #FFD700)", "#E6C200", "#4D4000", "#806A00", "🥇", "1st Place", df.iloc[0]["Student Name"], df.iloc[0]["Total (₹)"], df.iloc[0]["Coupons"], df.iloc[0]["Donations"]), unsafe_allow_html=True)
        if len(df) > 1: st.markdown(make_podium_card("linear-gradient(135deg, #F8F9FA, #E0E0E0)", "#BDBDBD", "#333333", "#666666", "🥈", "2nd Place", df.iloc[1]["Student Name"], df.iloc[1]["Total (₹)"], df.iloc[1]["Coupons"], df.iloc[1]["Donations"]), unsafe_allow_html=True)
        if len(df) > 2: st.markdown(make_podium_card("linear-gradient(135deg, #FFF0E6, #EBA87A)", "#CD7F32", "#5C3A21", "#8A5A33", "🥉", "3rd Place", df.iloc[2]["Student Name"], df.iloc[2]["Total (₹)"], df.iloc[2]["Coupons"], df.iloc[2]["Donations"]), unsafe_allow_html=True)

        # --- TOP 10 TABLE ---
        st.markdown("#### Top 10 Rankings")
        top_10_df = df.head(10).copy()
        display_df = top_10_df[['Student Name', 'Coupons', 'Donations', 'Total (₹)']]
        styled_df = display_df.style.background_gradient(subset=['Total (₹)'], cmap='Reds').format({"Total (₹)": "₹{:.0f}"})
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        st.info("💡 Only the Top 10 are shown here to keep things competitive!")

        st.divider()

        # --- INDIVIDUAL SEARCH TOOL ---
        with st.expander("🔍 Check Your Specific Stats"):
            search_query = st.text_input("Type your name to find your rank and totals:", placeholder="e.g., Muhammed")
            if search_query:
                user_result = df[df['Student Name'].str.contains(search_query, case=False, na=False)]
                if not user_result.empty:
                    user_result = user_result.copy()
                    user_result['Current Rank'] = user_result.index + 1
                    display_result = user_result[['Current Rank', 'Student Name', 'Coupons', 'Donations', 'Total (₹)']]
                    st.dataframe(display_result, use_container_width=True, hide_index=True)
                else:
                    st.warning("No records found. If you recently made a sale, please check your spelling or contact the admin.")