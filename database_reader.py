
import csv

def get_airport_prices(airport):
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    prices = {}

    airport = airport.upper().strip()

    for quarter in quarters:
        filename = f"data/{quarter}_2024.csv"

        with open(filename, "r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)

            for row in reader:
                if len(row) > 5 and row[1].strip() == airport:
                    prices[quarter] = float(row[5])
                    break

    return prices


# Test the database reader
if __name__ == "__main__":
    airport = input("Enter airport code: ")
    prices = get_airport_prices(airport)

    if prices:
        print(f"\n2024 Average Airfare for {airport.upper()}")

        for quarter, price in prices.items():
            print(f"{quarter}: ${price:.2f}")
    else:
        print("Airport not found.")
