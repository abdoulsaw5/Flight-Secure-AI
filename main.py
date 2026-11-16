
import subprocess
import sys

print("FLIGHT BOOKING AI SYSTEM")
print("========================")

print("\n1. AI 1 - Price-Based Assistant")
print("2. AI 2 - Security-Aware Assistant")
print("3. Website Security Checker")
print("4. Historical Flight Price Analyzer")

choice = input("\nChoose an option (1-4): ")

programs = {
    "1": "ai1.py",
    "2": "ai2.py",
    "3": "security_checker.py",
    "4": "price_analyzer.py"
}

if choice in programs:
    subprocess.run([sys.executable, programs[choice]])
else:
    print("Invalid option. Please choose 1-4.")
