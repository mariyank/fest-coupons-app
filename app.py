import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
import string
import base64
import os
from datetime import datetime

# --- BLOCK A: SETUP ---
st.set_page_config(page_title="Fest Lucky Coupon", layout="centered", initial_sidebar_state="collapsed")

# --- DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)
member_df = conn.read(worksheet="Members", ttl=0)

# --- HELPER: LOAD IMAGES FOR HTML ---
def load_image_base64(img_name):
    if os.path.exists(img_name):
        with open(img_name, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
            ext = "png" if img_name.lower().endswith(".png") else "jpeg"
            return f"data:image/{ext};base64,{encoded}"
    return ""

# --- BLOCK B: PREMIUM TICKET DISPLAY ---
if "ticket" in st.query_params:
    ticket_code = st.query_params["ticket"]
    
    # 1. HANDLE FESTIVAL COUPONS (LUCKY DRAW)
    if ticket_code.startswith("FEST-"):
        sales_df = conn.read(worksheet="Sales", ttl=0)
        match = sales_df[sales_df['Coupon Code'] == ticket_code]
        
        if not match.empty:
            buyer_name = match.iloc[0]['Buyer Name']
            buyer_mobile = match.iloc[0]['Mobile']
            
            # Load assets for the premium HTML ticket
            img_smrti = load_image_base64("smrti.png")
            img_muziris = load_image_base64("muziris.png")
            img_myg = load_image_base64("myg.png")
            img_luckydraw = load_image_base64("luckydraw.png")
            img_prizes = load_image_base64("prizes.png")

            # Masks
            m_base = "-webkit-mask-image: radial-gradient(circle at 0 0, transparent 16px, black 16.5px), radial-gradient(circle at 100% 0, transparent 16px, black 16.5px), radial-gradient(circle at 0 100%, transparent 16px, black 16.5px), radial-gradient(circle at 100% 100%, transparent 16px, black 16.5px); -webkit-mask-position: top left, top right, bottom left, bottom right; -webkit-mask-size: 51% 51%; -webkit-mask-repeat: no-repeat;"
            m_border = "-webkit-mask-image: radial-gradient(circle at 0 0, transparent 22px, black 22.5px), radial-gradient(circle at 100% 0, transparent 22px, black 22.5px), radial-gradient(circle at 0 100%, transparent 22px, black 22.5px), radial-gradient(circle at 100% 100%, transparent 22px, black 22.5px); -webkit-mask-position: top left, top right, bottom left, bottom right; -webkit-mask-size: 51% 51%; -webkit-mask-repeat: no-repeat;"
            m_inner = "-webkit-mask-image: radial-gradient(circle at 0 0, transparent 28px, black 28.5px), radial-gradient(circle at 100% 0, transparent 28px, black 28.5px), radial-gradient(circle at 0 100%, transparent 28px, black 28.5px), radial-gradient(circle at 100% 100%, transparent 28px, black 28.5px); -webkit-mask-position: top left, top right, bottom left, bottom right; -webkit-mask-size: 51% 51%; -webkit-mask-repeat: no-repeat;"
            
            # Mini Masks for ID Box
            mt_base = "-webkit-mask-image: radial-gradient(circle at 0 0, transparent 8px, black 8.5px), radial-gradient(circle at 100% 0, transparent 8px, black 8.5px), radial-gradient(circle at 0 100%, transparent 8px, black 8.5px), radial-gradient(circle at 100% 100%, transparent 8px, black 8.5px); -webkit-mask-position: top left, top right, bottom left, bottom right; -webkit-mask-size: 51% 51%; -webkit-mask-repeat: no-repeat;"
            mt_border = "-webkit-mask-image: radial-gradient(circle at 0 0, transparent 10px, black 10.5px), radial-gradient(circle at 100% 0, transparent 10px, black 10.5px), radial-gradient(circle at 0 100%, transparent 10px, black 10.5px), radial-gradient(circle at 100% 100%, transparent 10px, black 10.5px); -webkit-mask-position: top left, top right, bottom left, bottom right; -webkit-mask-size: 51% 51%; -webkit-mask-repeat: no-repeat;"
            mt_inner = "-webkit-mask-image: radial-gradient(circle at 0 0, transparent 12px, black 12.5px), radial-gradient(circle at 100% 0, transparent 12px, black 12.5px), radial-gradient(circle at 0 100%, transparent 12px, black 12.5px), radial-gradient(circle at 100% 100%, transparent 12px, black 12.5px); -webkit-mask-position: top left, top right, bottom left, bottom right; -webkit-mask-size: 51% 51%; -webkit-mask-repeat: no-repeat;"

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
            <div style="color:#E32636; flex-grow:1;"><h3 style="margin:0; font-size:14px;">MUZIRIS JMI</h3></div>
            <img src="{img_myg}" style="height:32px; background:white; padding:4px; border-radius:4px; border:1px solid #E32636;">
            </div>
            <img src="{img_luckydraw}" style="width:240px; margin-bottom:5px;">
            <div style="margin:10px auto 15px auto; position:relative; display:inline-block;">
            <div style="position:absolute; top:0; left:0; right:0; bottom:0; background:#088F8F; {mt_base} z-index:1;"></div>
            <div style="position:absolute; top:0; left:0; right:0; bottom:0; background:#8F0808; border:2px solid transparent; background-clip:padding-box; {mt_border} z-index:2;"></div>
            <div style="position:absolute; top:0; left:0; right:0; bottom:0; background:#088F8F; border:4px solid transparent; background-clip:padding-box; {mt_inner} z-index:3;"></div>
            <div style="position:relative; z-index:4; padding:8px 20px; color:white; font-size:18px; font-weight:bold;">No. {ticket_code}</div>
            </div>
            <div style="display:flex; justify-content:center; align-items:center; gap:8px;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#222" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg><span style="font-size:26px; font-family:'Aref Ruqaa', serif;">{buyer_name}</span></div>
            <div style="display:flex; justify-content:center; align-items:center; gap:8px;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#222" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg><span style="font-size:20px; font-family:'Amiri', serif;">{buyer_mobile}</span></div>
            <hr style="border-top: 2px dashed rgba(227,38,54,0.4); margin:15px 10px 10px 10px;">
            <h4 style="color:#E32636; margin:0 0 5px 0;">WIN EXCITING PRIZES!</h4>
            <img src="{img_prizes}" style="width:100%; border-radius:8px; border:1px solid rgba(227,38,54,0.2);">
            <p style="font-size:13px; color:#666; margin-top:8px;">🎟️ Present this digital pass at the entry gate.</p>
            </div></div>
            <div style="text-align:center; color:#E32636; font-size:18px; margin:-14px 0; position:relative; z-index:10; letter-spacing:4px;">✂ - - - - - - - - - -</div>
            <div style="background-color:#E32636; {m_base} padding:20px; text-align:center; position:relative;">
            <p style="color:#FFF9E6; font-size:12px; text-transform:uppercase; font-weight:bold; margin:0 0 8px 0;">Exclusive Sponsor Offer</p>
            <img src="{img_myg}" style="height:40px; background:white; padding:5px; border-radius:5px; margin-bottom:10px;">
            <div style="background:#FF6600; color:white; padding:10px; border-radius:8px; border:2px dashed white; font-weight:bold;">🎁 Use code JMIFEST30 for 30% OFF!</div>
            </div></div>
            """
            st.markdown(ticket_html, unsafe_allow_html=True)
            
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
                st.divider()
                st.warning("🎁 **Exclusive Sponsor Offer:** Get 30% off smart gadgets at MyG! Use code JMIFEST30.")
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