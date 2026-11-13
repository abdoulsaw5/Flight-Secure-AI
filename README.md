# Using Agentic AI to Improve Cybersecurity in Flight Booking

## Phase 1: Project Design and Scope

---

## 1. Project Overview

Our project focuses on developing an Agentic AI assistant that helps users find affordable flights while checking whether booking websites are safe and trustworthy. Many travelers focus on finding the cheapest flights without considering the cybersecurity risks associated with certain booking websites. Some websites may be fraudulent, have poor security practices, or have experienced data breaches. Our goal is to create a prototype that compares flight prices and website security information to help users make safer booking decisions.

We will develop two versions of the AI assistant to compare their performance.

### Group members
- Abdoul Sawadogo
- Boris
- Sadeq
- Ahmed
### AI 1: Price-Based Assistant

- Searches for the cheapest available flights.
- Compares prices from different booking websites.
- Recommends the cheapest option without considering cybersecurity risks.

### AI 2: Security-Aware Assistant

- Searches for affordable flights.
- Checks website legitimacy and security indicators.
- Reviews publicly reported data breaches.
- Checks whether security improvements have been reported.
- Flags potentially risky websites.
- Recommends affordable options with fewer identified security risks.

> **Privacy boundary:** The AI will not collect payment information, passport numbers, or other sensitive personal information. Users will make their own booking decision.

---

## 2. Project Metrics

We will use two main metrics to evaluate our project.

### Detection Rate

This measures how accurately AI 2 identifies risky booking websites.

**Formula:**

```
Detection Rate = (Risky Websites Correctly Flagged / Total Risky Websites) x 100
```

**Example:** If our dataset contains 10 risky websites and AI 2 correctly identifies 8:

```
Detection Rate = (8 / 10) x 100 = 80%
```

### Price Difference

This measures the difference between the flight prices recommended by AI 1 and AI 2.

**Formula:**

```
Price Difference = AI 2 Recommended Price - AI 1 Recommended Price
```

**Example:**

- AI 1 recommends a flight costing $250.
- AI 2 recommends a flight costing $275.

```
Price Difference = $275 - $250 = $25
```

This allows us to determine whether improved security comes at a higher cost.

### False Positives

We will also track false positives to see whether AI 2 incorrectly flags legitimate booking websites.

| Metric | What it tells us |
|---|---|
| Detection Rate | How well AI 2 catches risky websites |
| Price Difference | The cost of choosing the safer option |
| False Positives | How often AI 2 wrongly flags legitimate websites |

---

## 3. Research Articles

Ranked by how directly each article supports our implementation.

| Rank | Research article | What problem does it address? | How we will use it |
|---|---|---|---|
| 1 | AgentBound: Securing Execution Boundaries of AI Agents | AI agents may exceed their authorized permissions. | Restrict our AI to approved tools and prevent it from making purchases or handling payment details. |
| 2 | AI Agents Under Threat: A Survey of Key Security Challenges and Future Pathways | AI agents face threats from untrusted external content and complicated interactions. | Explain why flight-booking websites must be treated as untrusted information sources. |
| 3 | Agentic AI Security: Threats, Defenses, Evaluation, and Open Challenges | Prompt injection, tool misuse, and other Agentic AI vulnerabilities. | Design our security protections and attack-testing scenarios. |
| 4 | A Safety and Security Framework for Real-World Agentic Systems | Autonomous agents can take unsafe actions in real-world environments. | Build safeguards, security checks, and human approval requirements. |
| 5 | A Cybersecurity AI Agent Selection and Decision Support Framework | Selecting appropriate AI agents and autonomy levels. | Design how our assistant evaluates information and generates security recommendations. |
| 6 | Securing Agentic AI with the NIST Cybersecurity Framework 2.0 | Traditional cybersecurity frameworks need adaptation for Agentic AI. | Organize our security design around identifying, protecting against, detecting, and responding to risks. |
| 7 | Agentic AI for Cybersecurity: A Meta-Cognitive Architecture for Governable Autonomy | Autonomous cybersecurity decisions need oversight and governance. | Help our AI explain uncertain risk assessments and avoid overconfident recommendations. |
| 8 | Agentic AI as a Cybersecurity Attack Surface: Threats, Exploits, and Defenses in Runtime Supply Chains | AI tools and their execution environments introduce new attack surfaces. | Protect our assistant's interactions with external websites, tools, and APIs. |
| 9 | A Multi-Agent System for Cybersecurity Threat Detection and Correlation Using Large Language Models | Separate security indicators can be difficult to analyze together. | Design specialized agents for flight prices, website security, and breach research. |
| 10 | A Research Landscape of Agentic AI and Large Language Models: Applications, Challenges and Future Directions | Agentic AI applications have architectural, reliability, and trust challenges. | Explain the overall Agentic AI architecture and why a booking assistant is a useful application. |

---

## 4. How the 10 Articles Support Our Implementation

**Our flight-booking AI: research-to-implementation plan**

| Component | Purpose | Supported by |
|---|---|---|
| Flight Search Agent | Compare available flights and prices. | Articles 9 and 10 |
| Website Security Agent | Evaluate domain legitimacy, suspicious website signals, and potential attacks. | Articles 2, 3, 4, and 8 |
| Breach Research and Risk Agent | Review reported breaches, available remediation evidence, and uncertainty before generating a recommendation. | Articles 5, 6, and 7 (conceptual support) |
| Permission and Privacy Controls | Restrict tools, block automatic purchases, and keep payment information outside the assistant. | Articles 1, 3, and 4 |
