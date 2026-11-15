
import os
import requests
from datetime import date, timedelta
from dotenv import load_dotenv

# Load SerpApi key securely
load_dotenv()

API_KEY = os.getenv("SERPAPI_KEY")


def search_cheapest_flight():
    print("\n========== AI 1 ==========")
    print("Cheapest Flight Search")
    print("Security checks: DISABLED")
    print("==========================\n")

    if not API_KEY:
        print("ERROR: SERPAPI_KEY is missing from .env")
        return

    departure = input(
        "Departure airport (e.g. JFK): "
    ).strip().upper()

    arrival = input(
        "Destination airport (e.g. LAX): "
    ).strip().upper()

    default_date = (
        date.today() + timedelta(days=30)
    ).isoformat()

    travel_date = input(
        f"Departure date YYYY-MM-DD (default {default_date}): "
    ).strip() or default_date

    try:
        selected_date = date.fromisoformat(travel_date)
        if selected_date < date.today():
            print("Please choose a future date.")
            return
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    if (
        len(departure) != 3
        or len(arrival) != 3
        or not departure.isalpha()
        or not arrival.isalpha()
    ):
        print("Enter valid 3-letter airport codes.")
        return

    params = {
        "engine": "google_flights",
        "departure_id": departure,
        "arrival_id": arrival,
        "outbound_date": travel_date,
        "type": "2",
        "currency": "USD",
        "hl": "en",
        "api_key": API_KEY
    }

    print("\nAI 1 is searching Google Flights...\n")

    try:
        response = requests.get(
            "https://serpapi.com/search.json",
            params=params,
            timeout=45
        )

        response.raise_for_status()
        data = response.json()

        if "error" in data:
            print("API error:", data["error"])
            return

        offers = (
            data.get("best_flights", [])
            + data.get("other_flights", [])
        )

        offers = [
            offer for offer in offers
            if isinstance(offer.get("price"), (int, float))
        ]

        if not offers:
            print("No flights found.")
            return

        offers.sort(key=lambda offer: offer["price"])

        print("========== FLIGHT RESULTS ==========")

        for number, offer in enumerate(offers[:10], 1):
            segments = offer.get("flights", [])

            airlines = ", ".join(
                dict.fromkeys(
                    segment.get("airline", "Unknown")
                    for segment in segments
                )
            ) or "Unknown"

            price = offer["price"]
            duration = offer.get("total_duration", 0)
            stops = max(0, len(segments) - 1)

            print(f"\nFlight {number}")
            print("Airline:", airlines)
            print(f"Price: ${price}")
            print("Duration:", duration, "minutes")
            print("Stops:", stops)

        cheapest = offers[0]

        airlines = ", ".join(
            dict.fromkeys(
                segment.get("airline", "Unknown")
                for segment in cheapest.get("flights", [])
            )
        ) or "Unknown"

        print("\n========== AI 1 RECOMMENDATION ==========")
        print("Recommended airline:", airlines)
        print(f"Cheapest price: ${cheapest['price']}")
        print("Reason: Lowest listed price")
        print("Website security: NOT CHECKED")
        print("=========================================")

        print("\nPrices may change before booking.")
        print("The human makes the final booking decision.")

    except requests.RequestException as error:
        print("Connection error:", error)

    except ValueError:
        print("Could not read the API response.")


if __name__ == "__main__":
    search_cheapest_flight()
