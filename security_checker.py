
import os
import re
import requests

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SERPAPI_KEY")

TRUSTED_DOMAINS = {
    "jetblue.com": "JetBlue",
    "aa.com": "American Airlines",
    "delta.com": "Delta Air Lines",
    "united.com": "United Airlines",
    "booking.com": "Booking.com",
    "expedia.com": "Expedia",
    "google.com": "Google"
}

COMPANY_ALIASES = {
    "JetBlue": ["jetblue", "jetblue airways"],
    "American Airlines": ["american airlines"],
    "Delta Air Lines": ["delta air lines", "delta airlines"],
    "United Airlines": ["united airlines"],
    "Booking.com": ["booking.com"],
    "Expedia": ["expedia"],
    "Google": ["google"]
}

INCIDENT_PHRASES = [
    "data breach",
    "cyberattack",
    "cyber attack",
    "ransomware attack",
    "security breach",
    "unauthorized access",
    "customer data exposed",
    "personal information stolen"
]

ACTION_PHRASES = [
    "confirmed",
    "disclosed",
    "reported",
    "notified",
    "investigated",
    "suffered",
    "experienced",
    "affected"
]

GENERAL_RISK_PHRASES = [
    "could experience",
    "may experience",
    "risk of",
    "potential breach",
    "hypothetical",
    "how to prevent",
    "may suffer",
    "could suffer"
]


def get_domain(website):
    website = website.strip().lower()

    if not website.startswith(("http://", "https://")):
        website = "https://" + website

    parsed = urlparse(website)

    return (parsed.hostname or "").removeprefix("www.")


def identify_company(website):
    domain = get_domain(website)

    for official_domain, company in TRUSTED_DOMAINS.items():
        if (
            domain == official_domain
            or domain.endswith("." + official_domain)
        ):
            return company

    return None


def contains_phrase(text, phrase):
    pattern = (
        r"(?<!\w)"
        + re.escape(phrase)
        + r"(?!\w)"
    )

    return bool(
        re.search(pattern, text, re.IGNORECASE)
    )


def mentioned_companies(sentence):
    found = []

    for company, aliases in COMPANY_ALIASES.items():
        if any(
            contains_phrase(sentence, alias)
            for alias in aliases
        ):
            found.append(company)

    return found


def search_articles(company):
    if not API_KEY:
        print("ERROR: SERPAPI_KEY missing from .env")
        return []

    query = (
        f'"{company}" '
        '("data breach" OR "cyberattack" '
        'OR "ransomware attack") '
        '(confirmed OR disclosed OR reported)'
    )

    try:
        response = requests.get(
            "https://serpapi.com/search.json",
            params={
                "engine": "google",
                "q": query,
                "num": 10,
                "hl": "en",
                "api_key": API_KEY
            },
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        if "error" in data:
            print("Search error:", data["error"])
            return []

        return data.get("organic_results", [])

    except (requests.RequestException, ValueError) as error:
        print("Search failed:", error)
        return []


def download_article(url):
    parsed = urlparse(url)

    if parsed.scheme != "https":
        return None

    hostname = (parsed.hostname or "").lower()

    blocked_domains = [
        "google.com",
        "facebook.com",
        "reddit.com",
        "linkedin.com"
    ]

    if any(
        hostname == domain
        or hostname.endswith("." + domain)
        for domain in blocked_domains
    ):
        return None

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"},
            allow_redirects=False
        )

        if response.status_code != 200:
            return None

        content_type = response.headers.get(
            "Content-Type", ""
        ).lower()

        if "text/html" not in content_type:
            return None

        if len(response.content) > 1_000_000:
            return None

        soup = BeautifulSoup(
            response.content,
            "html.parser"
        )

        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside"
        ]):
            tag.decompose()

        article = soup.find("article")

        if article:
            text = article.get_text(" ", strip=True)
        else:
            main = soup.find("main")

            if main:
                text = main.get_text(" ", strip=True)
            else:
                text = soup.get_text(" ", strip=True)

        return re.sub(r"\s+", " ", text)[:30000]

    except requests.RequestException:
        return None


def analyze_article(text, company):
    if not text:
        return {
            "status": "UNAVAILABLE",
            "evidence": None
        }

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    for sentence in sentences:
        companies = mentioned_companies(sentence)

        # Reject ambiguous statements about multiple companies.
        if len(companies) != 1:
            continue

        if companies[0] != company:
            continue

        has_incident = any(
            contains_phrase(sentence, phrase)
            for phrase in INCIDENT_PHRASES
        )

        has_action = any(
            contains_phrase(sentence, phrase)
            for phrase in ACTION_PHRASES
        )

        general_risk = any(
            contains_phrase(sentence, phrase)
            for phrase in GENERAL_RISK_PHRASES
        )

        if (
            has_incident
            and has_action
            and not general_risk
        ):
            return {
                "status": "POSSIBLE INCIDENT",
                "evidence": sentence[:350]
            }

    return {
        "status": "NOT ESTABLISHED",
        "evidence": None
    }


def check_website(website):
    domain = get_domain(website)
    company = identify_company(website)

    print("\n========== SECURITY REPORT ==========")
    print("Website:", website)
    print("Domain:", domain)

    if not company:
        print("Official domain: NOT VERIFIED")
        print("Security risk: UNKNOWN")
        return

    print("Recognized company:", company)
    print("Official domain: RECOGNIZED")

    print("\nSearching for cybersecurity articles...")

    results = search_articles(company)

    checked = 0
    possible_incidents = 0

    for result in results:
        if checked >= 3:
            break

        url = result.get("link", "")
        article_text = download_article(url)

        if not article_text:
            continue

        checked += 1

        analysis = analyze_article(
            article_text, company
        )

        print(f"\n========== ARTICLE {checked} ==========")
        print("Title:", result.get("title", "Unknown"))
        print("Link:", url)
        print("Analysis:", analysis["status"])

        if analysis["evidence"]:
            print(
                "Possible evidence:",
                analysis["evidence"]
            )

        if analysis["status"] == "POSSIBLE INCIDENT":
            possible_incidents += 1

    print("\n========== FINAL ASSESSMENT ==========")
    print("Articles analyzed:", checked)
    print("Possible incidents flagged:", possible_incidents)
    print("Verified breach status: UNKNOWN")
    print("Verified remediation status: UNKNOWN")
    print("Overall security risk: UNKNOWN")
    print("Recommendation: MANUAL REVIEW REQUIRED")

    print(
        "\nMultiple-company statements are excluded "
        "from automatic incident detection."
    )
    print(
        "A single-company statement is still only "
        "a possible lead, not verified evidence."
    )

    print("======================================")


def main():
    print("\n=== AI 2 ARTICLE INVESTIGATION ===")

    website = input(
        "Enter website (e.g. jetblue.com): "
    ).strip()

    if not website:
        print("Please enter a website.")
        return

    check_website(website)


if __name__ == "__main__":
    main()
