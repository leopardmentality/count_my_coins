import os
import streamlit as st
import requests
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def import_blockchain_data(start_date, end_date):
    # Set the API endpoint URL
    url = "https://api.coincap.io/v2/assets"

    # Get the API key from the Streamlit secrets
    api_key = st.secrets["COINCAP_API_KEY"]

    # Set the headers to include the API key
    headers = {
        "X-CoinCap-API-Key": api_key
    }

    # Set the query parameters for the start and end dates
    params = {
        "start": start_date.isoformat(),
        "end": end_date.isoformat()
    }

    # Send a GET request to the CoinCap API
    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the data from the response
        data = response.json()["data"]

        # Extract the relevant data
        names = [coin["name"] for coin in data]
        prices = [float(coin["priceUsd"]) for coin in data]
        change_percents = [float(coin["changePercent24Hr"]) for coin in data]

        # Convert the data to NumPy arrays
        names = np.array(names)
        prices = np.array(prices)
        change_percents = np.array(change_percents)

        return names, prices, change_percents
    else:
        print("Error: Could not retrieve data from the API")
        return None, None, None

def get_top_coins(names, change_percents, n=3):
    # Find the top n coins by average change percent
    top_indices = np.argsort(change_percents)[-n:]
    top_names = names[top_indices]
    top_change_percents = change_percents[top_indices]
    return top_names, top_change_percents, top_indices

def main():
    st.title("Count My Coins")

    # Get the start and end dates for the past 6 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)

    # Call the import_blockchain_data function with the start and end dates
    names, prices, change_percents = import_blockchain_data(start_date, end_date)

    # Check if the data is as expected
    if names is not None and prices is not None and change_percents is not None:
        # Get the top 3 coins by average change percent
        top_names, top_change_percents, top_indices = get_top_coins(names, change_percents)

        # Prepare the data for XGBoost
        scaler = MinMaxScaler(feature_range=(0, 1))
        X = scaler.fit_transform(prices.reshape(-1, 1))
        y = np.repeat([prices[-1]], len(X))

        # Define the XGBoost model
        model = XGBRegressor()

        # Train the XGBoost model
        model.fit(X, y)

        # Calculate the potential earnings
        initial_investment = 10000
        potential_earnings = []
        for i in range(len(top_names)):
            predicted_price = model.predict(scaler.transform([[prices[top_indices[i]]]]))
            percent_change = (predicted_price[0] - prices[top_indices[i]]) / prices[top_indices[i]] * 100
            earnings = initial_investment * (1 + percent_change / 100)
            potential_earnings.append(earnings)

        # Display the top 3 coins, their change percent, and potential earnings
        st.write("Top 3 coins by average change percent:")
        for name, change_percent, earnings in zip(top_names, top_change_percents, potential_earnings):
            st.write(f"{name}, Change Percent: {change_percent:.2f}%, Potential Earnings: ${earnings:.2f}")

        # Create the potential earnings chart
        fig = make_subplots(rows=1, cols=1, vertical_spacing=0.2)
        fig.add_trace(
            go.Bar(
                x=top_names,
                y=potential_earnings,
                marker_color='#1f77b4'
            ),
            row=1, col=1
        )

        fig.update_layout(
            title='Potential Earnings on $10,000 Investment',
            xaxis_title='Coin',
            yaxis_title='Potential Earnings (USD)',
            font=dict(
                family="Courier New, monospace",
                size=14,
                color="RebeccaPurple"
            )
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("\nData not as expected.")

if __name__ == "__main__":
    main()
