Sure, here's the updated README document with the requested changes:

# Count My Coins

This code is designed to predict the potential earnings of investing in the top 3 cryptocurrencies based on their 24-hour price change percentage. It uses the CoinCap API to retrieve cryptocurrency data for the past 6 months, processes it using scikit-learn and XGBoost libraries, and displays the results in a Streamlit web application.

## Features

- Retrieves cryptocurrency data from the CoinCap API for the past 6 months
- Finds the top 3 cryptocurrencies based on their 24-hour price change percentage
- Calculates the potential earnings of investing $10,000 in each of the top 3 cryptocurrencies
- Displays the top 3 cryptocurrencies, their 24-hour price change percentage, and potential earnings
- Creates a bar chart showing the potential earnings for each of the top 3 cryptocurrencies

## Dependencies

- Python 3.x
- Streamlit
- Requests
- NumPy
- scikit-learn
- XGBoost
- Plotly

## Usage

1. Clone the repository or download the code files.
2. Install the required dependencies using pip: `pip install -r requirements.txt`.
3. Obtain an API key from CoinCap and store it in an environment variable named `COINCAP_API_KEY`.
4. Run the Streamlit application using the command: `streamlit run app.py`.
5. The application will open in your default web browser.
6. The application will display the top 3 cryptocurrencies, their 24-hour price change percentage, and potential earnings based on a $10,000 investment for the past 6 months.
7. A bar chart showing the potential earnings for each of the top 3 cryptocurrencies will also be displayed.

## Code Structure

The code is structured into three main parts:

1. **Data retrieval**: The `import_blockchain_data()` function retrieves cryptocurrency data from the CoinCap API for the past 6 months.

2. **Data processing**: The `get_top_coins()` function finds the top 3 cryptocurrencies based on their 24-hour price change percentage. The `main()` function prepares the data for XGBoost, trains the model, and calculates the potential earnings.

3. **User interface**: The `main()` function also displays the top 3 cryptocurrencies, their 24-hour price change percentage, and potential earnings using Streamlit. It creates a bar chart showing the potential earnings using Plotly.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- CoinCap API for providing cryptocurrency data
- Streamlit for enabling the creation of interactive web applications
- Plotly for providing powerful data visualization capabilities
