import streamlit as st
import yfinance as yf
import datetime

st.set_page_config(page_title="MarketSage Analyst GPT", layout="centered")

st.title("📈 MarketSage Analyst GPT")
st.subheader("AI-powered stock market analyst for Indian markets")
st.markdown("Try tickers like `INFY.NS`, `RELIANCE.NS`, `TCS.NS`, `LAURUSLABS.NS`, etc.")

ticker = st.text_input("Enter NSE Ticker (with .NS)", value="INFY.NS")

if ticker:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="max")

        if hist.empty:
            st.warning(f"⚠️ No data available for {ticker}")
        else:
            ltp = hist["Close"].iloc[-1]
            ath = hist["Close"].max()
            sma_50 = hist["Close"].rolling(50).mean().iloc[-1]
            sma_200 = hist["Close"].rolling(200).mean().iloc[-1]
            company_name = stock.info.get("longName", "N/A")
            today = datetime.datetime.now().strftime("%Y-%m-%d")

            verdict = []

            # ATH Analysis
            if ltp >= ath:
                verdict.append("✅ All-Time High")
            elif abs(ltp - ath) / ath <= 0.005:
                verdict.append("✅ Near All-Time High (within 0.5%)")
            else:
                verdict.append("❌ Not at ATH")

            # Trend Analysis
            if ltp > sma_50 and ltp > sma_200:
                verdict.append("✅ Uptrend (SMA 50 & 200)")
            else:
                verdict.append("❌ No SMA uptrend")

            # Display
            st.markdown(f"""
            ### 📊 MarketSage Report – {ticker} [{today}]
            - **Company:** {company_name}
            - **LTP:** ₹{ltp:.2f}
            - **ATH (Max):** ₹{ath:.2f}
            - **SMA 50:** ₹{sma_50:.2f}
            - **SMA 200:** ₹{sma_200:.2f}

            **🔍 Analysis:** {" | ".join(verdict)}

            > 📘 For Informational Purposes Only
            """)
    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
