import pandas as pd
import numpy as np

def extract_data():
    # Load the CSV file
    df = pd.read_csv('wig20_d.csv')

    # Extract the 'Data' and 'Zamkniecie' columns
    data_from_file = df[['Data', 'Zamkniecie']]

    return data_from_file

data = extract_data()
print(data) # Print the data

def calculate_ema(_data, _n):
    """
    Calculate the Exponential Moving Average (EMA) of a given data set for the last n periods
    Parameters
    ----------
    _data : list of float or int from newest (at index=0) to oldest (at index=n-1)
    _n : int, the number of periods to consider in the EMA calculation

    Returns
    -------
    numpy array of EMA values
    should return values for each data point in the given period
    """
    alpha = 2 / (_n + 1)  # Calculate the smoothing factor alpha, 2/(N+1)

    # Calculate the EMA
    ema_values = []  # Create an array to store the EMA values

    # Initialize the first EMA value as the first data point
    ema_values.append(_data[0])

    for i in range(_n*2, len(_data)):
        # Calculate the exponential average by using the formula
        window_average = round((alpha * _data[i]) + (1 - alpha) * ema_values[-1], 2)

        # Store the cumulative average of current window in moving average list
        ema_values.append(window_average)

    return ema_values

# Extract the 'Zamkniecie' column
closing_prices = data['Zamkniecie'].values

# Calculate the EMA_26
ema26 = calculate_ema(closing_prices, 26)

# Calculate the EMA_12
ema12 = calculate_ema(closing_prices, 12)

# Print the EMA values as regular floats
for value in ema26:
    print(float(value))
print(len(ema26))

for value in ema12:
    print(float(value))
print(len(ema12))