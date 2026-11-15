
import os
import requests
from datetime import date, timedelta
from dotenv import load_dotenv

from security_checker import get_domain, TRUSTED_DOMAINS

load_dotenv()
API_KEY = os.getenv("SERPAPI_KEY")

# These are airline website references, NOT confirmed booking providers.
AIRLINE_WEBSITES = {
    "JetBlue": "https://www.jetblue.com",
    "American": "https://www.aa.com",
    "American Airlines": "https://www.aa.com",
    "Delta": "https://www.delta.com",
    "Delta Air Lines": "https://www.delta.com",
    "United": "https://www.united.com",
    "United Airlines": "https://www.united.com"
}


def check_airline_domain(airline):
    website = AIRLINE_WEBSITES.get(airline)

    if not website:
        return {
            "website": "Unknown",
            "domain_status": "NOT VERIFIED",
            "security_risk": "UNKNOWN"
        }

    domain = get_domain(website)

    recognized = any(
        domain == trusted
        or domain.endswith("." + trusted)
        for trusted in TRUSTED_DOMAINS
    )

    return {
        "website": website,
        "domain_status": (
            "RECOGNIZED" if recognized else "NOT VERIFIED"
        ),
        "security_risk": "UNKNOWN"
    }


def search_secure_flights():
    print("\n========== AI 2 ==========")
    print("Flight Search + Security Evaluation")
    print("==========================")

    if not API_KEY:
        print("ERROR: SERPAPI_KEY is missing from .env")
        return

    departure = input(
        "\nDeparture airport (e.g. JFK): "
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

    if not (
        len(departure) == 3
        and departure.isalpha()
        and len(arrival) == 3
        and arrival.isalpha()
    ):
        print("Please enter valid 3-letter airport codes.")
        return

    try:
        selected_date = date.fromisoformat(travel_date)

        if selected_date < date.today():
            print("Please choose a future date.")
            return

    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
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

        offers = (
            data.get("best_flights", [])
            + data.get("other_flights", [])
        )

        offers = [
            offer for offer in offers
            if isinstance(offer.get("price"), (int, float))
        ]

        if not offers:
            print("No flight offers found.")
            return

        offers.sort(key=lambda offer: offer["price"])

        print("\n========== FLIGHT RESULTS ==========")

        for number, offer in enumerate(offers[:10], 1):
            segments = offer.get("flights", [])

            airlines = list(dict.fromkeys(
                segment.get("airline", "Unknown")
                for segment in segments
            ))

            print(f"\nFlight {number}")
            print("Airline:", ", ".join(airlines))
            print(f"Price: ${offer['price']}")
            print(
                "Duration:",
                offer.get("total_duration", "N/A"),
                "minutes"
            )
            print("Stops:", max(0, len(segments) - 1))

            for airline in airlines:
                security = check_airline_domain(airline)

                print("\nAirline:", airline)
                print("Airline website:", security["website"])
                print(
                    "Official domain:",
                    security["domain_status"]
                )

            print("Actual booking provider: NOT IDENTIFIED")
            print("Data breach status: NOT CHECKED")
            print("Security risk: UNKNOWN")

        cheapest = offers[0]

        print("\n========== AI 2 REPORT ==========")
        print(f"Lowest flight price: ${cheapest['price']}")
        print("Airline domain checking: COMPLETED")
        print("Booking provider checking: PENDING")
        print("Data breach investigation: PENDING")
        print("Security recommendation: NOT AVAILABLE")

        print("\nAI 2 cannot confirm which offer is safest yet.")
        print("No flight was booked.")
        print("The human makes the final decision.")

    except requests.RequestException as error:
        print("Connection error:", error)

    except ValueError:
        print("Could not read the API response.")


if __name__ == "__main__":
    search_secure_flights()
