
import csv

quarters = ["Q1", "Q2", "Q3", "Q4"]

airport = input("Enter airport code (JFK, LAX, LGA): ").upper().strip()

print(f"\n2024 Average Airfare for {airport}")
print("--------------------------------")

prices = []

for quarter in quarters:
    filename = f"data/{quarter}_2024.csv"

    with open(filename, "r", encoding="utf-8-sig") as file:
        reader = csv.reader(file)

        for row in reader:
            if len(row) > 5 and row[1].strip() == airport:
                price = float(row[5])
                prices.append((quarter, price))

                print(f"{quarter}: ${price:.2f}")
                break

if prices:
    cheapest = min(prices, key=lambda item: item[1])

    print("\nLowest Historical Average Fare:")
    print(f"Quarter: {cheapest[0]}")
    print(f"Average Fare: ${cheapest[1]:.2f}")
else:
    print("Airport not found in the database.")
