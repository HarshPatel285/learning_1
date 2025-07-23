import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

# Streamlit UI
st.title("📈 Yahoo Finance - Linear Regression on Stock Prices")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA):", "AAPL")
period = st.selectbox("Select Period:", ["1mo", "3mo", "6mo", "1y", "2y"])
interval = st.selectbox("Select Interval:", ["1d", "1wk", "1mo"])

if st.button("Run Regression"):
    df = yf.download(ticker, period=period, interval=interval)
    if df.empty:
        st.warning("No data returned. Try another ticker or range.")
    else:
        df.dropna(inplace=True)
        df.reset_index(inplace=True)

        # Convert date to numeric (ordinal format)
        df['Date_Ordinal'] = df['Date'].map(pd.Timestamp.toordinal)

        # Prepare X and y
        X = df[['Date_Ordinal']]
        y = df['Close']

        # Fit model
        model = LinearRegression()
        model.fit(X, y)

        # Predict
        y_pred = model.predict(X)

        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df['Date'], y, label="Actual", color='blue')
        ax.plot(df['Date'], y_pred, label="Linear Regression", color='red')
        ax.set_title(f"{ticker} Close Price & Regression Line")
        ax.set_xlabel("Date")
        ax.set_ylabel("Close Price ($)")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)

        # Display coefficients
        st.markdown(f"**Regression Equation:**")
        slope = float(model.coef_[0])
        intercept = float(model.intercept_)
        st.code(f"Price = {slope:.4f} * Date + {intercept:.2f}")
