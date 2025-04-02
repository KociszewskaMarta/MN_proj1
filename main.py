import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def save_plot(filename):
    """
    Save the plot as a PNG file
    Parameters
    ----------
    filename : str, the filename to save the plot as
    """
    plt.savefig(filename)

def extract_data():
    """
    Extract the 'Data' and 'Zamkniecie' columns from the CSV file
    Returns
    -------
    data : pandas.DataFrame, the extracted data from the CSV file with 'Data' and 'Zamkniecie' columns
    """
    # Load the CSV file
    df = pd.read_csv('wig20_d.csv')

    # Convert the 'Data' column to datetime format
    df['Data'] = pd.to_datetime(df['Data'])

    # Extract the 'Data' and 'Zamkniecie' columns
    data_from_file = df[['Data', 'Zamkniecie']]

    return data_from_file

def plot_data(data):
    """
    Plot the data
    Parameters
    ----------
    data

    Returns
    -------

    """
    plt.figure(figsize=(28, 10))
    plt.plot(data['Data'], data['Zamkniecie'], label='Ceny zamknięcia', color='black')

    # Set the x-axis to display dates only at the start of each month
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

    # Rotate the x-axis labels to be vertical
    plt.xticks(rotation=90)

    plt.xlabel('Data')
    plt.ylabel('Cena zamknięcia (PLN)')
    plt.title('Wykres giełdowy dla WIG20 2020-10-01 - 2025-03-12', fontsize=20)
    plt.legend()
    # save_plot('graphs/closing_prices.png')
    # plt.show()

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

def plot_macd_and_signal(data, macd, signal):
    """
    Plot the MACD and Signal Line
    Parameters
    ----------
    data
    macd
    signal

    Returns
    -------

    """
    plt.figure(figsize=(28, 10))
    plt.plot(data['Data'][-len(macd):], macd, label='MACD', color='blue')
    plt.plot(data['Data'][-len(signal):], signal, label='Signal Line', color='red')

    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=90)

    plt.xlabel('Data')
    # plt.ylabel('Value')
    plt.title('Wykres MACD / SIGNAL dla WIG20', fontsize=20)
    plt.legend()
    # save_plot("graphs/macd_and_signal.png")
    # plt.show()

def plot_histogram(data, macd, signal):
    """

    Parameters
    ----------
    data
    macd
    signal

    Returns
    -------

    """
    histogram = macd[:len(signal)] - signal
    plt.figure(figsize=(28, 10))
    plt.bar(data['Data'][-len(histogram):], histogram, label='Histogram', color='green', alpha=1)

    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=90)

    plt.xlabel('Data')
    plt.ylabel('Wartość MACD')
    plt.title('Histogram MACD dla WIG20', fontsize=20)
    plt.legend()
    # save_plot("graphs/histogram.png")
    # plt.show()

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


def plot_macd_signal_and_cross_points(data, macd, signal, cross_points):
    """
    Plot the MACD, Signal Line, and Cross Points
    Parameters
    ----------
    data
    macd
    signal
    cross_points

    Returns
    -------

    """
    plt.figure(figsize=(28, 10))
    plt.plot(data['Data'][-len(macd):], macd, label='MACD', color='blue')
    plt.plot(data['Data'][-len(signal):], signal, label='Signal Line', color='red')

    cross_dates = [data['Data'].iloc[-len(macd) + point[0]] for point in cross_points]
    cross_values = [point[1] for point in cross_points]

    plt.scatter(cross_dates, cross_values, color='green', marker='o', label='Cross Points')

    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=90)

    plt.xlabel('Data')
    # plt.ylabel('Value')
    plt.title('Wykres MACD / SIGNAL dla WIG20 z zaznaczonymi punktami przecięcia', fontsize=20)
    plt.legend()
    # save_plot("graphs/macd_signal_cross_points.png")
    # plt.show()

def calculate_buy_sell_signals(macd, signal):
    """
    Calculate the buy and sell signals based on the MACD and Signal Line
    Buy and Sell signals are calculated as follows:
    - Buy Signal: MACD crosses above the Signal Line
    - Sell Signal: MACD crosses below the Signal Line
    Parameters
    ----------
    macd : numpy array of MACD values
    signal : numpy array of Signal Line values

    Returns
    -------
    buy_signals : list of tuples containing the index and value of the buy signals
    sell_signals : list of tuples containing the index and value of the sell signals
    """
    buy_signals = []
    sell_signals = []
    for i in range(1, len(macd)):
        if macd[i] > signal[i] and macd[i - 1] < signal[i - 1]:
            buy_signals.append((i, macd[i]))
        elif macd[i] < signal[i] and macd[i - 1] > signal[i - 1]:
            sell_signals.append((i, macd[i]))
    return buy_signals, sell_signals

def plotting_buy_sell_signals(data, macd, signal, buy_signals, sell_signals):
    """
    Plot the MACD, Signal Line,Buy Signals, and Sell Signals
    Parameters
    ----------
    data
    macd
    signal
    buy_signals
    sell_signals

    Returns
    -------

    """
    plt.figure(figsize=(28, 10))
    plt.plot(data['Data'][-len(macd):], macd, label='MACD', color='blue', linewidth=1, linestyle='--')
    plt.plot(data['Data'][-len(signal):], signal, label='Signal Line', color='red', linewidth=1, linestyle='--')

    buy_dates = [data['Data'].iloc[-len(macd) + point[0]] for point in buy_signals]
    buy_values = [point[1] for point in buy_signals]
    sell_dates = [data['Data'].iloc[-len(macd) + point[0]] for point in sell_signals]
    sell_values = [point[1] for point in sell_signals]

    plt.scatter(buy_dates, buy_values, color='green', marker='^', label='Buy Signals')
    plt.scatter(sell_dates, sell_values, color='red', marker='v', label='Sell Signals')

    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=90)

    plt.xlabel('Data')
    # plt.ylabel('Value')
    plt.title('Wykres MACD / SIGNAL dla WIG20 z zaznaczonymi sygnałami kupna i sprzedaży', fontsize=20)
    plt.legend()
    # save_plot("graphs/macd_signal_buy_sell_points.png")
    # plt.show()

def save_plot_with_dates(filename, start_date, end_date):
    """
    Save the plot as a PNG file with dates in the filename
    Parameters
    ----------
    filename : str, the base filename to save the plot as
    start_date : str, the start date to include in the filename
    end_date : str, the end date to include in the filename
    """
    formatted_filename = f"{filename}_{start_date}_{end_date}.png"
    plt.savefig(formatted_filename)

def plotting_buy_sell_signals_for_given_period(data, macd, signal, buy_signals, sell_signals, starting_date, ending_date):
    """
    Plot the MACD, Signal Line, Buy Signals, and Sell Signals for a given period
    Parameters
    ----------
    data
    macd
    signal
    buy_signals
    sell_signals
    starting_date
    ending_date

    Returns
    -------

    """
    starting_date = pd.to_datetime(starting_date)
    ending_date = pd.to_datetime(ending_date)

    # Filter the data for the given period
    mask = (data['Data'] >= starting_date) & (data['Data'] <= ending_date)
    filtered_data = data.loc[mask]

    # Calculate the indices for the filtered data
    start_idx = data.index.get_loc(filtered_data.index[0])
    end_idx = data.index.get_loc(filtered_data.index[-1]) + 1

    # Filter the MACD and Signal values for the given period
    filtered_macd = macd[start_idx:end_idx]
    filtered_signal = signal[start_idx:end_idx]

    plt.figure(figsize=(28, 10))
    plt.plot(filtered_data['Data'], filtered_macd, label='MACD', color='blue', linewidth=1, linestyle='--')
    plt.plot(filtered_data['Data'], filtered_signal, label='Signal Line', color='red', linewidth=1, linestyle='--')

    buy_dates = [data['Data'].iloc[point[0]] for point in buy_signals if starting_date <= data['Data'].iloc[point[0]] <= ending_date]
    buy_values = [point[1] for point in buy_signals if starting_date <= data['Data'].iloc[point[0]] <= ending_date]
    sell_dates = [data['Data'].iloc[point[0]] for point in sell_signals if starting_date <= data['Data'].iloc[point[0]] <= ending_date]
    sell_values = [point[1] for point in sell_signals if starting_date <= data['Data'].iloc[point[0]] <= ending_date]

    plt.scatter(buy_dates, buy_values, color='green', marker='^', label='Buy Signals')
    plt.scatter(sell_dates, sell_values, color='red', marker='v', label='Sell Signals')

    # Add text for buy signals
    for date, value in zip(buy_dates, buy_values):
        closing_price = data.loc[data['Data'] == date, 'Zamkniecie'].values[0]
        plt.text(date, value, f'{closing_price:.2f}', color='green', fontsize=10, ha='center', va='bottom')

    # Add text for sell signals
    for date, value in zip(sell_dates, sell_values):
        closing_price = data.loc[data['Data'] == date, 'Zamkniecie'].values[0]
        plt.text(date, value, f'{closing_price:.2f}', color='red', fontsize=10, ha='center', va='top')

    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=90)

    plt.xlabel('Data')
    plt.title(
        f'Wykres MACD / SIGNAL dla WIG20 dla okresu od {starting_date.strftime("%Y-%m-%d")} do {ending_date.strftime("%Y-%m-%d")}', fontsize=20)
    plt.legend()
    save_plot_with_dates("graphs/macd_signal_buy_sell_points_for_", starting_date.strftime('%Y-%m-%d'), ending_date.strftime('%Y-%m-%d'))
    plt.show()

# ---------------------------------------------------
# Main code

# Extract the data
data = extract_data()
print(data) # Print the datas

plot_data(data)

# Extract the 'Zamkniecie' column
closing_prices = data['Zamkniecie'].values

# Calculate the MACD
macd = calculate_macd(closing_prices)

# Calculate the Signal Line
signal = calculate_signal(macd)

# to make macd and signal the same length
macd = macd[len(macd) - len(signal):]

# Calculate the cross points
cross_points = cross(macd, signal)

# plot the data
plot_macd_and_signal(data, macd, signal)

# Plot the histogram on a different graph
plot_histogram(data, macd, signal)

# Plot the MACD, Signal Line, and Cross Points
plot_macd_signal_and_cross_points(data, macd, signal, cross_points)

# Calculate the buy and sell signals
buy_signals, sell_signals = calculate_buy_sell_signals(macd, signal)

# Plot the MACD, Signal Line, Buy Signals, and Sell Signals
plotting_buy_sell_signals(data, macd, signal, buy_signals, sell_signals)

# Plot the MACD, Signal Line, Buy Signals, and Sell Signals for a given period
plotting_buy_sell_signals_for_given_period(data, macd, signal, buy_signals, sell_signals, '2021-02-01', '2021-03-15')

plotting_buy_sell_signals_for_given_period(data, macd, signal, buy_signals, sell_signals, '2023-07-01', '2023-08-31')

plotting_buy_sell_signals_for_given_period(data, macd, signal, buy_signals, sell_signals, '2024-01-01', '2024-01-31')

plotting_buy_sell_signals_for_given_period(data, macd, signal, buy_signals, sell_signals, '2020-10-01', '2021-01-31')

plotting_buy_sell_signals_for_given_period(data, macd, signal, buy_signals, sell_signals, '2022-06-01', '2022-09-30')

plotting_buy_sell_signals_for_given_period(data, macd, signal, buy_signals, sell_signals, '2023-10-01', '2023-12-31')

plotting_buy_sell_signals_for_given_period(data, macd, signal, buy_signals, sell_signals, '2021-01-15', '2021-02-04')








