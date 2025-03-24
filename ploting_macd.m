% Load CSV file
data = readtable('wig20_d.csv'); % Replace with your actual file name

% Extract closing prices
closing_prices = data.Zamkniecie; % Adjust column name if different

% Compute MACD and Signal Line
[macdLine, signalLine] = macd(closing_prices);

% Plot the MACD indicator
% Create figure with a custom size
figure('Units', 'pixels', 'Position', [100, 100, 1200, 400]); % 3200x400 pixels (wider)
plot(macdLine, 'b', 'LineWidth', 1); hold on;
plot(signalLine, 'r', 'LineWidth', 1);
legend('MACD Line', 'Signal Line');
title('MACD Indicator');
xlabel('Time');
ylabel('Value');
grid on;

% Save the figure
saveas(gcf, 'macd_plot_by_matlab.png'); % Save as PNG
