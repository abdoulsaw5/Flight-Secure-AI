

import os
import requests
from datetime import date, timedelta
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

API_KEY = os.getenv("SERPAPI_KEY")


def search_flights():
    if not API_KEY:
        print("ERROR: SERPAPI_KEY is missing from .env")
        return

    print("\n=== Google Flights Search ===")

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
        parsed_date = date.fromisoformat(travel_date)

        if parsed_date < date.today():
            print("Please choose a future date.")
            return

    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    if len(departure) != 3 or len(arrival) != 3:
        print("Please enter valid 3-letter airport codes.")
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

    print("\nSearching Google Flights...")

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

        flights = (
            data.get("best_flights", [])
            + data.get("other_flights", [])
        )

        if not flights:
            print("No flight offers found for this search.")
            return

        flights.sort(
            key=lambda flight: flight.get(
                "price", float("inf")
            )
        )

        print("\n=== Available Flight Offers ===")

        for number, offer in enumerate(
            flights[:10], start=1
        ):
            segments = offer.get("flights", [])

            airlines = ", ".join(
                dict.fromkeys(
                    segment.get("airline", "Unknown")
                    for segment in segments
                )
            )

            price = offer.get("price", "N/A")
            duration = offer.get("total_duration", "N/A")
            stops = max(0, len(segments) - 1)

            print(f"\nFlight {number}")
            print("Airline:", airlines)
            print("Price: $", price)
            print("Duration:", duration, "minutes")
            print("Stops:", stops)

        cheapest = flights[0]

        print("\n=== Cheapest Flight ===")
        print("Price: $", cheapest.get("price", "N/A"))
        print("\nPrices may change before booking.")
        print("No personal information was submitted.")

    except requests.RequestException as error:
        print("Connection error:", error)

    except ValueError:
        print("Could not read the API response.")


if __name__ == "__main__":
    search_flights()
