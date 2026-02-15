import tkinter as tk
from tkinter import messagebox
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ---------- FUNCTION TO PREDICT STOCK ----------
def predict_stock():
    ticker_symbol = entry.get().upper()

    if ticker_symbol == "":
        messagebox.showerror("Error", "Please enter a stock ticker symbol!")
        return

    try:
        # Download stock data (last 1 year)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        data = yf.download(ticker_symbol, start=start_date, end=end_date)

        if data.empty:
            messagebox.showerror("Error", "Invalid Ticker Symbol!")
            return

        # Prepare Data
        data['Prediction'] = data['Close'].shift(-10)
        X = np.array(data[['Close']][:-10])
        y = np.array(data['Prediction'][:-10])

        # Train Model
        model = LinearRegression()
        model.fit(X, y)

        # Predict next 10 days
        X_future = np.array(data[['Close']][-10:])
        predictions = model.predict(X_future)

        # Display Prediction
        result_label.config(text=f"Predicted Price (Next Day): ${predictions[-1]:.2f}")

        # Plot Graph
        plt.figure(figsize=(10,5))
        plt.plot(data['Close'], label="Actual Price", color="purple")
        plt.plot(range(len(data)-10, len(data)), predictions, label="Predicted", color="pink")
        plt.title(f"{ticker_symbol} Stock Prediction")
        plt.legend()
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------- GUI DESIGN ----------
app = tk.Tk()
app.title("Stock Market Predictor ")
app.geometry("500x300")
app.configure(bg="#4B0082")  # Indigo / Purple

title = tk.Label(app, text="Stock Market Predictor",
                 font=("Helvetica", 18, "bold"),
                 bg="#4B0082", fg="#FF69B4")
title.pack(pady=20)

entry = tk.Entry(app, font=("Helvetica", 14),
                 bg="#FFC0CB", fg="#4B0082", justify="center")
entry.pack(pady=10)

predict_button = tk.Button(app, text="Predict Stock Price",
                           font=("Helvetica", 12, "bold"),
                           bg="#FF69B4", fg="white",
                           command=predict_stock)
predict_button.pack(pady=15)

result_label = tk.Label(app, text="Prediction will appear here",
                        font=("Helvetica", 14),
                        bg="#4B0082", fg="#FFC0CB")
result_label.pack(pady=20)

app.mainloop()
