import streamlit as st
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Streamlit UI
st.title("📊 Yahoo Finance Boxplot Viewer")

ticker = st.text_input("Enter Stock Ticker Symbol (e.g., AAPL, TSLA):", "AAPL")
period = st.selectbox("Select Time Period:", ["1mo", "3mo", "6mo", "1y", "2y", "5y"])
interval = st.selectbox("Select Interval:", ["1d", "1wk", "1mo"])

if st.button("Generate Boxplot"):
    try:
        df = yf.download(ticker, period=period, interval=interval)
        if df.empty:
            st.warning("No data returned. Please check the ticker or try a different time range.")
        else:
            df.dropna(inplace=True)

            st.write(f"Showing data for **{ticker}** - Close Prices")

            # Plotting
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.boxplot(y=df['Close'], ax=ax)
            ax.set_title(f'{ticker} Close Price Boxplot ({period})')
            ax.set_ylabel('Price ($)')
            st.pyplot(fig)
    except Exception as e:
        st.error(f"Error: {e}")
