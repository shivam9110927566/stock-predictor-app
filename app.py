import asyncio
import sys
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Windows Proactor fix
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

st.set_page_config(page_title="AI Stock Predictor Pro Enterprise", page_icon="📈", layout="wide")

API_URL = "http://127.0.0.1:8000"

if "user_id" not in st.session_state:
    st.session_state.user_id = 0
if "username" not in st.session_state:
    st.session_state.username = ""

# --- SIDEBAR AUTH ---
st.sidebar.title("🔐 Enterprise Portal")
if st.session_state.user_id == 0:
    auth_mode = st.sidebar.radio("Action", ["Login", "Sign Up"])
    u_name = st.sidebar.text_input("Username")
    u_pass = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Submit"):
        if u_name and u_pass:
            endpoint = f"{API_URL}/auth/signup" if auth_mode == "Sign Up" else f"{API_URL}/auth/login"
            try:
                res = requests.post(endpoint, json={"username": u_name, "password": u_pass}).json()
                if res.get("status") == "success":
                    st.sidebar.success(res["message"])
                    if auth_mode == "Login":
                        st.session_state.user_id = res["user_id"]
                        st.session_state.username = res["username"]
                        st.rerun()
                else:
                    st.sidebar.error(res.get("message", "Error"))
            except Exception as e:
                st.sidebar.error(f"Server offline: {e}")
        else:
            st.sidebar.warning("Enter all fields")
else:
    st.sidebar.success(f"User: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.user_id = 0
        st.session_state.username = ""
        st.rerun()

# --- MAIN APP ---
st.title("📈 AI Stock Predictor Pro Enterprise Terminal")
st.markdown("Advanced Multi-User Indian Stock Analytics, Paper Trading & AI Advisory Ecosystem")

if st.session_state.user_id == 0:
    st.warning("⚠️ Please Login or Sign Up from the sidebar to access full terminal features.")
else:
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "AI Prediction & Upload 🤖", 
        "Comparison ⚖️", 
        "Watchlist ⭐", 
        "Paper Trading 💵", 
        "AI Screener 🔍",
        "AI Assistant 💡"
    ])
    
    with tab1:
        st.subheader("📊 Live Ticker Analysis & Vision AI Upload")
        col1, col2 = st.columns(2)
        with col1:
            ticker_input = st.text_input("Stock Ticker (e.g., RELIANCE.NS, TCS.NS, SBIN.NS):", "RELIANCE.NS")
        with col2:
            period_choice = st.selectbox("Timeframe", ["1mo", "3mo", "6mo", "1y"], index=1)
            
        if st.button("Run AI Prediction"):
            with st.spinner("Processing deep learning LSTM & technical oscillators..."):
                try:
                    res = requests.get(f"{API_URL}/predict/{ticker_input}?period={period_choice}&user_id={st.session_state.user_id}").json()
                    if res.get("status") == "success":
                        st.success("Analysis Complete!")
                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("Current Price", f"₹{res['current_price']}")
                        c2.metric("AI Target", f"₹{res['predicted_close_price']}")
                        c3.metric("RSI (14)", f"{res['rsi']}")
                        c4.metric("Risk / Reward", res['risk_reward'])
                        
                        st.info(f"🤖 **AI Advisory:** {res['ai_advice']}")
                        st.write(f"🛑 **Stop Loss:** ₹{res['stop_loss']}")
                        st.write(f"🎯 **Target Price:** ₹{res['target_price']}")
                        st.write(f"📌 **RSI Status:** {res['rsi_status']}")
                        st.write(f"⚡ **MACD Status:** {res['macd_status']}")
                        st.write(f"📰 **Market Sentiment:** {res['sentiment_mood']}")
                    else:
                        st.error("Prediction failed.")
                except Exception as e:
                    st.error(f"Connection error: {e}")
                    
        st.markdown("---")
        st.subheader("📁 Upload Financial Report / Chart Screenshot")
        uploaded_file = st.file_uploader("Upload Image/CSV", type=["csv", "png", "jpg", "jpeg"])
        if uploaded_file is not None:
            if st.button("🚀 Analyze Uploaded Graphic"):
                with st.spinner("Computer Vision AI scanning chart patterns..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        res = requests.post(f"{API_URL}/predict/upload?user_id={st.session_state.user_id}", files=files).json()
                        if res.get("status") == "success":
                            st.success("Scan Successful!")
                            u1, u2, u3 = st.columns(3)
                            u1.metric("Ref Price", f"₹{res['current_price']}")
                            u2.metric("Target", f"₹{res['predicted_close_price']}")
                            u3.metric("Risk/Reward", res['risk_reward'])
                            st.info(res['ai_advice'])
                    except Exception as e:
                        st.error(f"Error: {e}")

    with tab2:
        st.subheader("⚖️ Multi-Stock Comparative Analysis")
        s1 = st.text_input("Stock Alpha", "RELIANCE.NS")
        s2 = st.text_input("Stock Beta", "TCS.NS")
        if st.button("Compare Strengths"):
            res = requests.get(f"{API_URL}/compare?stock1={s1}&stock2={s2}").json()
            if res.get("status") == "success":
                st.success("Comparison Report Generated:")
                st.write(res["comparison"])

    with tab3:
        st.subheader("⭐ Real-Time Watchlist")
        new_w = st.text_input("Add Ticker", "TATAMOTORS.NS")
        if st.button("Add to Watchlist"):
            res = requests.post(f"{API_URL}/watchlist/add/{new_w}?user_id={st.session_state.user_id}").json()
            st.success(res.get("message"))
            
        w_res = requests.get(f"{API_URL}/watchlist?user_id={st.session_state.user_id}").json()
        if w_res.get("status") == "success":
            for item in w_res.get("watchlist", []):
                st.write(f"🌟 **{item['stock']}** — ₹{item['current_price']} ({item['change_percent']}%)")

    with tab4:
        st.subheader("💵 Paper Trading Simulation Dashboard")
        p_stock = st.text_input("Order Ticker", "SBIN.NS")
        p_shares = st.number_input("Quantity", min_value=1, value=25)
        p_price = st.number_input("Execution Price", min_value=1.0, value=780.0)
        if st.button("Execute Buy Order"):
            res = requests.post(f"{API_URL}/paper/buy?stock={p_stock}&shares={p_shares}&price={p_price}&user_id={st.session_state.user_id}").json()
            if res.get("status") == "success":
                st.success(res["message"])
            else:
                st.error(res.get("message"))
                
        port = requests.get(f"{API_URL}/paper/portfolio?user_id={st.session_state.user_id}").json()
        if port.get("status") == "success":
            m1, m2, m3 = st.columns(3)
            m1.metric("Virtual Cash Balance", f"₹{port['balance']:,.2f}")
            m2.metric("Total Net Worth", f"₹{port['net_worth']:,.2f}")
            m3.metric("Aggregate P&L", f"₹{port['total_pnl']:,.2f}")
            
            st.write("### Active Portfolio Holdings")
            if port["portfolio"]:
                df_port = pd.DataFrame(port["portfolio"])
                st.dataframe(df_port, use_container_width=True)
                
                # Export option
                csv_data = df_port.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Export Portfolio CSV", csv_data, "my_portfolio.csv", "text/csv")
            else:
                st.info("No active open positions in portfolio.")

    with tab5:
        st.subheader("🔍 AI Stock Screener & Signal Scanner")
        if st.button("Scan Market Indices"):
            scan = requests.get(f"{API_URL}/screener/scan").json()
            if scan.get("status") == "success":
                df_scr = pd.DataFrame(scan["screener"])
                st.dataframe(df_scr, use_container_width=True)

    with tab6:
        st.subheader("💡 AI Financial Assistant & Strategy Chat")
        user_query = st.text_input("Ask AI about risk management, swing trading, or options strategies:")
        if st.button("Ask AI"):
            if user_query:
                st.info(f"🤖 **AI Strategist Response:** For your query regarding *'{user_query}'*, always maintain a strict 1:2 risk-to-reward ratio, use trailing stop losses, and avoid risking more than 2% of your total capital on a single trade setup.")
            else:
                st.warning("Please type a query first.")
