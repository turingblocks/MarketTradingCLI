import argparse
import random
from colorama import Fore, Style, init

init()

class StockBroker:
    def __init__(self, balance=10000):
        self.balance = balance
        self.portfolio = {}  # Dictionary to store owned shares: {"company_name": shares}
        self.transaction_history = []  # List to store transaction history: [(action, company_name, shares, price)]

    def buy(self, company_name, shares, price):
        cost = shares * price
        if cost <= self.balance:
            self.balance -= cost
            if company_name in self.portfolio:
                self.portfolio[company_name] += shares
            else:
                self.portfolio[company_name] = shares
            self.transaction_history.append(("BUY", company_name, shares, price))
            return True
        else:
            return False

    def sell(self, company_name, shares, price):
        if company_name in self.portfolio and self.portfolio[company_name] >= shares:
            earnings = shares * price
            self.balance += earnings
            self.portfolio[company_name] -= shares
            self.transaction_history.append(("SELL", company_name, shares, price))
            return True
        else:
            return False

    def show_balance(self):
        return self.balance

    def show_portfolio(self):
        return self.portfolio

    def show_transaction_history(self):
        return self.transaction_history

def generate_random_price_change(current_price):
    return current_price * random.uniform(0.9, 1.1)

def calculate_return(initial_price, current_price):
    return (current_price - initial_price) / initial_price * 100

def display_stock_price(company, price, initial_price):
    if price > initial_price:
        color = Fore.GREEN
    elif price < initial_price:
        color = Fore.RED
    else:
        color = Style.RESET_ALL

    print(f"{company}: {color}{price:.2f}{Style.RESET_ALL}")

def main():
    # Example companies and initial stock prices
    companies = {
        "Apple": 150,
        "Google": 2500,
        "Microsoft": 300,
        "Amazon": 3200,
        "Facebook": 350,
        "Tesla": 700,
        "Netflix": 550,
        "Adobe": 600,
        "Nvidia": 800,
        "Intel": 50,
    }

    initial_prices = {company: price for company, price in companies.items()}

    parser = argparse.ArgumentParser(description="Wolf of Wall Street - Stock Market Game")
    parser.add_argument("--balance", type=float, default=10000, help="Starting balance (default: 10000)")
    args = parser.parse_args()

    broker = StockBroker(balance=args.balance)

    while True:
        print("------ Ticker Board ------")
        for company, price in companies.items():
            display_stock_price(company, price, initial_prices[company])

        print("\n------ Your Information ------")
        print(f"Current Balance: {broker.show_balance():.2f}")

        total_investment = 0
        total_current_value = 0

        for company, shares in broker.show_portfolio().items():
            price = companies.get(company, 0)
            if price > 0:
                display_stock_price(company, price, initial_prices[company])
                investment = shares * price
                total_investment += investment
                total_current_value += (investment + calculate_return(initial_prices[company], price))

        if total_investment > 0:
            profit_loss_percent = (total_current_value - total_investment) / total_investment * 100
        else:
            profit_loss_percent = 0

        print(f"\nTotal Investment: {total_investment:.2f}")
        print(f"Total Current Value: {total_current_value:.2f}")
        print(f"P/L (%): {profit_loss_percent:.2f}%")

        action = input("\nWhat would you like to do? (buy, sell, balance, portfolio, history, quit): ").lower()

        if action == "buy":
            company = input("Enter the company name: ")
            shares = int(input("Enter the number of shares to buy: "))
            price = companies.get(company, 0)
            if price > 0:
                if broker.buy(company, shares, price):
                    print(f"Bought {shares} shares of {company} at {price:.2f} each.")
                else:
                    print("Insufficient balance to make the purchase.")
            else:
                print("Invalid company name.")

        elif action == "sell":
            company = input("Enter the company name: ")
            shares = int(input("Enter the number of shares to sell: "))
            price = companies.get(company, 0)
            if price > 0:
                if broker.sell(company, shares, price):
                    print(f"Sold {shares} shares of {company} at {price:.2f} each.")
                else:
                    print("Not enough shares to make the sale.")
            else:
                print("Invalid company name.")

        elif action == "balance":
            print(f"Your current balance: {broker.show_balance():.2f}")

        elif action == "portfolio":
            print("------ Portfolio ------")
            for company, shares in broker.show_portfolio().items():
                print(f"{company}: {shares} shares")

        elif action == "history":
            print("------ Transaction History ------")
            for entry in broker.show_transaction_history():
                action, company, shares, price = entry
                print(f"{action} - {company}: {shares} shares at {price:.2f} each")

        elif action == "quit":
            print("Thank you for playing!")
            break

        else:
            print("Invalid action. Please try again.")

        # Simulate random price changes for each company
        for company in companies:
            companies[company] = generate_random_price_change(companies[company])

if __name__ == "__main__":
    main()
