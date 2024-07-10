from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import csv
import json
from datetime import datetime
import yfinance as yf


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Função para ler o arquivo CSV enviado pelo formulário
def read_csv(file):
    data = []
    try:
        stream = file.stream
        csv_data = csv.DictReader(stream, delimiter=';')
        data = [row for row in csv_data]
    except Exception as e:
        print(f'Error reading CSV file: {e}')
    return data


def get_current_price(ticker):
    try:
        ticker_data = yf.Ticker(ticker)
        current_price = ticker_data.history(period='1d')['Close'].iloc[-1]  # Last closing price
        return current_price
    except Exception as e:
        print(f'Error fetching price for {ticker}: {e}')
        return None

# Função para gerar o arquivo JSON a partir dos dados do CSV
def generate_json(data):
    total_portfolio_value = 0.0
    total_invested_funds = 0.0
    portfolio_by_broker = {}

    for stock in data:
        ticker = stock['ticker']
        avg_buy_value = float(stock['Average Buy Value'].replace(',', '.'))
        number_of_shares = float(stock['Number of shares'].replace(',', '.'))
        current_price = get_current_price(ticker)

        if current_price:
            total_stock_value = current_price * number_of_shares
            total_portfolio_value += total_stock_value
            total_investment_value = avg_buy_value * number_of_shares
            total_invested_funds += total_investment_value
            broker = stock['Broker']

            if broker not in portfolio_by_broker:
                portfolio_by_broker[broker] = {
                    'Total Portfolio Value': 0.0,
                    'Total Investment (€)': 0.0,
                    'Stocks': []
                }

            portfolio_by_broker[broker]['Stocks'].append({
                'Name': stock['Name'],
                'Ticker': ticker,
                'Total Investment (€)': format(total_investment_value, '.2f'),
                'Average Buy Value (€)': format(avg_buy_value, '.2f'),
                'Number of shares': format(number_of_shares, '.2f'),
                'Total Stock Value (€)': format(total_stock_value, '.2f')
            })

            portfolio_by_broker[broker]['Total Portfolio Value'] += total_stock_value
            portfolio_by_broker[broker]['Total Investment (€)'] += total_investment_value

    statistics = {
        'Name': f'Statistics_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}',
        'Total Portfolio Value (€)': format(total_portfolio_value, '.2f'),
        'Total Invested Funds (€)': format(total_invested_funds, '.2f'),
        'Portfolio by Broker': portfolio_by_broker
    }

    return statistics

# Função para salvar o arquivo JSON
def save_json(user_id, statistics):
    user_directory = os.path.join('data', 'user_data', user_id)
    os.makedirs(user_directory, exist_ok=True)
    filename = f'{statistics["Name"]}.json'
    filepath = os.path.join(user_directory, filename)

    with open(filepath, 'w', encoding='utf-8') as jsonfile:
        json.dump(statistics, jsonfile, indent=4, ensure_ascii=False)

    return filename

# Rota inicial - exibe o menu inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para upload do arquivo CSV
@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            data = read_csv(file)
            if not data:
                flash('Error reading CSV file')
                return redirect(request.url)

            user_id = 'user_1'  # Simulação de um ID de usuário
            statistics = generate_json(data)
            filename = save_json(user_id, statistics)
            flash(f'File {filename} successfully uploaded and processed')
            return redirect(url_for('success'))

    return render_template('upload.html')

# Rota para exibir a página de sucesso
@app.route('/success')
def success():
    return render_template('success.html')

# Rota para exibir o histórico do portfólio
@app.route('/portfolio_history')
def portfolio_history():
    user_id = 'user_1'
    user_directory = f'data/user_data/{user_id}'

    try:
        # Check if the user directory exists; create if it doesn't
        if not os.path.exists(user_directory):
            os.makedirs(user_directory)

        # Now list the files in the user's directory
        portfolio_files = os.listdir(user_directory)

        # Return a JSON response with the list of portfolio files
        return jsonify(portfolio_files)

    except FileNotFoundError:
        os.abort(404, description=f"User directory '{user_id}' not found.")
    except Exception as e:
        os.abort(500, description=str(e))

if __name__ == '__main__':
    app.run(debug=True)
