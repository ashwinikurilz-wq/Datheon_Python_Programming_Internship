
import csv
import os

DATA_FILE = "sp500_tickers.csv"
OUTPUT_FILE = "portfolio_summary.csv"


def load_tickers():

    tickers = []

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    ticker = row[0].strip().upper()

                    # Skip blank cells and common header names
                    if ticker and ticker not in {
                        "SYMBOL", "TICKER", "TICKER SYMBOL"
                    }:
                        tickers.append(ticker)

    return sorted(set(tickers))


def get_positive_number(message):

    while True:
        try:
            number = float(input(message))
            if number > 0:
                return number
            print("Enter a number greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    tickers = load_tickers()

    print("=" * 48)
    print("     STOCK PORTFOLIO PERFORMANCE TRACKER")
    print("=" * 48)

    if tickers:
        print(f"Loaded {len(tickers)} ticker symbols from {DATA_FILE}.")
    else:
        print("Ticker dataset not found or empty.")
        print("You can still enter a ticker manually.")

    portfolio = []

    while True:
        ticker = input("\nEnter stock ticker (or DONE to finish): ")
        ticker = ticker.strip().upper()

        if ticker == "DONE":
            break

        if not ticker:
            print("Ticker cannot be empty.")
            continue

        if tickers and ticker not in tickers:
            print("Ticker not found in the loaded dataset.")
            print("Please enter a listed ticker.")
            continue

        buy_price = get_positive_number("Enter purchase price per share: ")
        quantity = get_positive_number("Enter number of shares: ")


        current_price = get_positive_number(
            "Enter current price per share (sample/manual price): "
        )

        invested = buy_price * quantity
        market_value = current_price * quantity
        gain_loss = market_value - invested
        percentage = (gain_loss / invested) * 100

        portfolio.append({
            "Ticker": ticker,
            "Buy Price": round(buy_price, 2),
            "Quantity": quantity,
            "Current Price": round(current_price, 2),
            "Invested Capital": round(invested, 2),
            "Market Value": round(market_value, 2),
            "Gain/Loss": round(gain_loss, 2),
            "Gain/Loss (%)": round(percentage, 2)
        })

    if not portfolio:
        print("\nNo stock holdings entered. No summary generated.")
        return

    total_invested = sum(item["Invested Capital"] for item in portfolio)
    total_value = sum(item["Market Value"] for item in portfolio)
    total_gain_loss = total_value - total_invested
    total_percentage = (total_gain_loss / total_invested) * 100

    print("\n" + "=" * 48)
    print("PORTFOLIO SUMMARY")
    print("=" * 48)

    for item in portfolio:
        print(
            f'{item["Ticker"]}: '
            f'Invested = {item["Invested Capital"]:.2f}, '
            f'Market Value = {item["Market Value"]:.2f}, '
            f'Gain/Loss = {item["Gain/Loss"]:.2f} '
            f'({item["Gain/Loss (%)"]:.2f}%)'
        )

    print("-" * 48)
    print(f"Total invested: {total_invested:.2f}")
    print(f"Total market value: {total_value:.2f}")
    print(f"Total gain/loss: {total_gain_loss:.2f}")
    print(f"Overall return: {total_percentage:.2f}%")


    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = list(portfolio[0].keys())
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(portfolio)

    print(f"\nSummary saved to: {os.path.abspath(OUTPUT_FILE)}")


if __name__ == "__main__":
    main()
