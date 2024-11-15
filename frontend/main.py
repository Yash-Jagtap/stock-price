import streamlit as st
import websocket
import json
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
st.set_page_config(page_title="Real-Time Stock Tracker", layout="wide")
# Function to fetch data via REST API
def fetch_stock_price(user_input):

    # Fetch stock price using requests
    response = requests.get(f"http://localhost:8000/stock/{user_input}")
    if response.status_code == 200:
        data = response.json()
        if "price" in data:
            st.metric("Stock Price", f"${data['price']}")
        else:
            st.error(data.get("error", "Unknown error occurred"))
    else:
        st.error("Failed to fetch data from the server.")






# WebSocket connection
def websocket_data(symbol):
    ws_url = f"ws://localhost:8000/ws/{symbol}"
    ws = websocket.WebSocket()
    ws.connect(ws_url)
    return ws



# Create a form
with st.form(key='stock_form'):
    # Input box for user to enter stock symbol
    symbol = st.text_input("Enter Stock Symbol:")
    
    # Submit button for the form
    submit_button = st.form_submit_button(label='Get Stock Price')


if submit_button:
    if symbol:
        # Your logic to fetch stock data goes here
        st.write(f"Fetching data for {symbol}...")
        data = fetch_stock_price(symbol)
        st.write(data)
        # Here you would call your backend to get the stock data
    else:
        st.error("Please enter a valid stock symbol.")






# Button to fetch and create the chart
if st.button("Create Chart"):
    st.write("Fetching data from the backend...")

    try:

        # Fetch data from the backend API
        response = requests.get(f'http://localhost:8000/getall/{symbol}')
        
        if response.status_code == 200:
            stock_data = response.json()  # Parse JSON response
            df = pd.DataFrame(stock_data)

            # Convert the timestamp column to datetime for Altair
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            # Streamlit app setup
            st.title("📈 Stock Price Chart")
            chart = (
            alt.Chart(df)
            .mark_line(color="red")  # Line color
            .encode(
                x=alt.X("timestamp:T", axis=alt.Axis(title="Time", format="%H:%M")),  # Format to hours
                y=alt.Y("price:Q", axis=alt.Axis(title="Price (USD)")),
                tooltip=["timestamp:T", "price:Q"]  # Tooltip to show timestamp and price
            )
            .properties(width=800, height=400)  # Set width and height of the chart
        )

        # Overlay points on the line
            points = (
                alt.Chart(df)
                .mark_point(color="red", filled=True, size=30)  # Dots on the line
                .encode(
                    x="timestamp:T",
                    y="price:Q",
                    tooltip=["timestamp:T", "price:Q"]
                )
            )

            # Combine line and points
            final_chart = (chart + points).interactive()  # Enable zoom and pan

            # Display the chart
            st.altair_chart(final_chart, use_container_width=True)
        else:
            st.error(f"Failed to fetch data. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")










# UI
# st.title("📈 Real-Time Stock Price Tracker")
# symbol = st.text_input("Enter Stock Symbol:", "AAPL")
# data = None
# if user_input != None:
#     data = fetch_stock_price(user_input)
#     # Display static data
# col1, col2 = st.columns(2)
# col1.subheader("Latest Stock Price")
# # data = fetch_stock_price(symbol)
# if "price" in data:
#     col1.metric("Price", f"${data['price']}")
# else:
#     col1.error(data["error"])
# if symbol:
#     st_autorefresh(interval=5000, key="autorefresh")
#     col1, col2 = st.columns(2)

#     # Display static data
#     col1.subheader("Latest Stock Price")
#     data = fetch_stock_price(symbol)
#     if "price" in data:
#         col1.metric("Price", f"${data['price']}")
#     else:
#         col1.error(data["error"])

#     # Display real-time updates
#     col2.subheader("Live Updates")
#     try:
#         ws = websocket_data(symbol)
#         live_data = json.loads(ws.recv())
#         if "price" in live_data:
#             col2.metric("Live Price", f"${live_data['price']}")
#         else:
#             col2.warning("Waiting for updates...")
#     except Exception as e:
#         col2.error("WebSocket connection failed.")
