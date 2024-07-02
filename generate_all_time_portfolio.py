import os
import json
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

# Directory containing the JSON files. Historic directory.
directory = ''

# Function to read JSON files from the directory
def read_json_files(directory):
    portfolio_history = []

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                portfolio_history.append(data)

    return portfolio_history

# Function to parse the date from the file name
def parse_date_from_name(name):
    date_str = name.split('_')[1] + '_' + name.split('_')[2]
    return datetime.strptime(date_str, '%Y-%m-%d_%H-%M-%S')

# Function to group data by month and get the last entry of each month
def get_monthly_history(portfolio_history):
    monthly_history = defaultdict(list)

    for record in portfolio_history:
        date = parse_date_from_name(record['Name'])
        month_key = date.strftime('%Y-%m')
        monthly_history[month_key].append((date, record))

    # Select the last record of each month
    final_monthly_history = {
        month: max(records, key=lambda x: x[0])[1] for month, records in monthly_history.items()
    }

    return final_monthly_history

# Function to transform and visualize portfolio history
def transform_and_visualize_history(portfolio_history):
    # Sort the portfolio history by date
    portfolio_history.sort(key=lambda x: parse_date_from_name(x['Name']))

    # Extract data for plotting
    dates = [parse_date_from_name(record['Name']) for record in portfolio_history]
    total_values = [float(record['Total Portfolio Value (€)'].replace(',', '')) for record in portfolio_history]
    total_investments = [float(record['Total Invested Funds (€)'].replace(',', '')) for record in portfolio_history]
    total_profits = [float(record['Total Profit (€)'].replace(',', '')) for record in portfolio_history]
    total_losses = [float(record['Total Loss (€)'].replace(',', '')) for record in portfolio_history]

    # Plot the historical data
    plt.figure(figsize=(12, 8))
    plt.plot(dates, total_values, label='Total Portfolio Value (€)', marker='o')
    plt.plot(dates, total_investments, label='Total Invested Funds (€)', marker='o')
    plt.plot(dates, total_profits, label='Total Profit (€)', marker='o')
    plt.plot(dates, total_losses, label='Total Loss (€)', marker='o')

    # Annotate each point with its value
    for i, date in enumerate(dates):
        plt.annotate(f'{total_values[i]:,.2f}', (date, total_values[i]), textcoords="offset points", xytext=(0,10), ha='center')

    # Annotate each point with its value for Total Invested Funds (€)
    for i, date in enumerate(dates):
        plt.annotate(f'{total_investments[i]:,.2f}', (date, total_investments[i]), textcoords="offset points", xytext=(0,10), ha='center')

    plt.xlabel('Date')
    plt.ylabel('Amount (€)')
    plt.title('Historical Transformation of My Portfolio')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Main function to run the script
def main():
    portfolio_history = read_json_files(directory)
    transform_and_visualize_history(portfolio_history)

if __name__ == '__main__':
    main()
