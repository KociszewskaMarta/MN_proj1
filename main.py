import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def extract_data():
    """
    Extract the 'Data' and 'Zamkniecie' columns from the CSV file
    Returns
    -------
    data : pandas.DataFrame, the extracted data from the CSV file with 'Data' and 'Zamkniecie' columns
    """
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

    for i in range(_n, len(_data)):
        # Calculate the exponential average by using the formula
        window_average = round((alpha * _data[i]) + (1 - alpha) * ema_values[-1], 2)

        # Store the cumulative average of current window in moving average list
        ema_values.append(window_average)

    return ema_values

def pad_ema(ema, length):
    """
    Pad the EMA values with None to match the length of the data
    Parameters
    ----------
    ema
    length

    Returns
    -------
    list of EMA values padded with None
    """
    return [None] * (length - len(ema)) + ema

def calculate_macd(_data, n1=12, n2=26):
    """
    Calculate the Moving Average Convergence Divergence (MACD) of a given data set
    Parameters
    ----------
    _data : list of float or int from newest (at index=0) to oldest (at index=n-1)
    N1 : int, the number of periods to consider in the EMA calculation for EMA1
    N2 : int, the number of periods to consider in the EMA calculation for EMA2

    Returns
    -------
    numpy array of MACD values
    should return values for each data point in the given period
    """
    # Calculate the EMA for N1 periods
    ema12 = calculate_ema(_data, n1)

    # Calculate the EMA for N2 periods
    ema26 = calculate_ema(_data, n2)

    max_length = max(len(ema12), len(ema26))
    ema12 = pad_ema(ema12, max_length)
    ema26 = pad_ema(ema26, max_length)

    # Calculate the MACD as the difference between the two EMAs
    macd_values = [e1 - e2 if e1 is not None and e2 is not None else None for e1, e2 in zip(ema12, ema26)]
    # zip() pairs the elements into tuples
    # e1 - e2 calculates the difference between the two elements in each tuple
    # if e1 is not None and e2 is not None else None checks if both elements are not None
    # if they are not None, it calculates the difference, otherwise it returns None

    #macd_values = np.array(ema1) - np.array(ema2)

    macd_values = macd_values[n2-n1:]
    macd_values = np.array(macd_values)
    return macd_values


def calculate_signal(_macd, n3=9):
    """
    Calculate the Signal Line of the MACD
    Parameters
    ----------
    _macd : numpy array of MACD values

    Returns
    -------
    numpy array of Signal Line values
    should return values for each data point in the given period
    """
    # Calculate the EMA for 9 periods
    signal_line = calculate_ema(_macd, n3)
    signal_line = np.array(signal_line)

    return signal_line

def plot_macd_and_signal(macd, signal):
    plt.figure(figsize=(28, 7))
    plt.plot(macd, label='MACD', color='red')
    plt.plot(signal, label='Signal Line', color='blue')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('MACD and Signal Line')
    plt.legend()
    plt.show()

def plot_histogram(macd, signal):
    # Calculate the histogram
    histogram = macd[:len(signal)] - signal
    plt.figure(figsize=(28, 7))
    plt.bar(range(len(histogram)), histogram, label='Histogram', color='green', alpha=1)
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Histogram')
    plt.legend()
    plt.show()

def cross(macd, signal):
    """
    Calculate the cross points between the MACD and Signal Line
    Parameters
    ----------
    macd : numpy array of MACD values
    signal : numpy array of Signal Line values

    Returns
    -------
    list of tuples containing the index and value of the cross points
    """
    cross_points = []
    for i in range(1, len(macd)):
        if (macd[i] > signal[i] and macd[i - 1] < signal[i - 1]) or (macd[i] < signal[i] and macd[i - 1] > signal[i - 1]):
            cross_points.append((i, macd[i]))
    return cross_points

def plot_cross_points(data, cross_points):
    plt.figure(figsize=(28, 7))
    plt.plot(data, label='Data', color='black')
    plt.scatter([point[0] for point in cross_points], [point[1] for point in cross_points], color='red', marker='o', label='Cross Points')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Cross Points')
    plt.legend()
    plt.show()

# Extract the 'Zamkniecie' column
closing_prices = data['Zamkniecie'].values

# # Calculate the EMA_26
# ema26 = calculate_ema(closing_prices, 26)
#
# # Calculate the EMA_12
# ema12 = calculate_ema(closing_prices, 12)

# Print the EMA values as regular floats
# for value in ema26:
#     print(float(value))
# print(len(ema26))

# for value in ema12:
#     print(float(value))
# print(len(ema12))

# Calculate the MACD
macd = calculate_macd(closing_prices)

# Print the MACD values as regular floats
print("MACD values:")
for value in macd:
    print(float(value))
print("Length of macd",len(macd))

# Calculate the Signal Line
signal = calculate_signal(macd)

# Print the Signal Line values as regular floats
print("Signal values:")
for value in signal:
    print(float(value))
print("Length of signal",len(signal))

macd=macd[:len(signal)]

# plot the data
plot_macd_and_signal(macd, signal)

# Plot the histogram on a different graph
plot_histogram(macd, signal)

# Calculate the cross points
cross_points = cross(macd, signal)

# Print the cross points
print("Cross points:")
for point in cross_points:
    print(point)





