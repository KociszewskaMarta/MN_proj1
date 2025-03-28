# Program to calculate exponential
# moving average using formula

import numpy as np

arr = [1, 2, 3, 7, 9]
x = 0.5  # smoothening factor

i = 1
# Initialize an empty list to
# store exponential moving averages
moving_averages = []

# Insert first exponential average in the list
moving_averages.append(arr[0])

# Loop through the array elements
while i < len(arr):
    # Calculate the exponential
    # average by using the formula
    window_average = round((x * arr[i]) +
                           (1 - x) * moving_averages[-1], 2)

    # Store the cumulative average
    # of current window in moving average list
    moving_averages.append(window_average)

    # Shift window to right by one position
    i += 1

print(moving_averages)