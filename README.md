# Silhouette Design Store – Home Page UI Automation

This repository provides an automated test suite for the **Silhouette Design Store Home Page** ([https://www.silhouettedesignstore.com/](https://www.silhouettedesignstore.com/)).

The framework is built with **Python**, **Playwright**, and **Pytest**, adhering strictly to the **Page Object Model (POM)** pattern.

---

## Directory Structure

```
Silhouette AI Automation/
├── pages/
│   ├── __init__.py
│   ├── base_page.py           # Core Playwright wrapper methods
│   └── home_page.py           # Home Page object actions and interactions
├── locators/
│   ├── __init__.py
│   └── home_locators.py       # Stable Home Page UI selectors
├── tests/
│   ├── __init__.py
│   └── home/
│       ├── __init__.py
│       └── test_home_page.py  # Structured test scenarios top to bottom
├── utils/
│   ├── __init__.py
│   ├── logger.py              # Custom logging utility
│   ├── screenshot_manager.py  # Failure screenshot capture
│   └── result_tracker.py      # Element verification audit tracker
├── reports/
│   └── home_page_report.html  # Self-contained pytest HTML report
├── screenshots/               # Failure & evidence screenshots
├── logs/
│   └── automation.log         # Execution log file
├── conftest.py                # Pytest fixtures and hooks
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Dependencies
└── README.md
```

---

## Setup & Prerequisites

1. Python 3.10+ installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

---

## Running Tests

### Run All Home Page Tests
```bash
pytest
```
Or run the home test file directly:
```bash
pytest tests/home/test_home_page.py
```

### Run an Individual Test Case
```bash
pytest tests/home/test_home_page.py::TestHomePageElements::test_02_header_elements
```

---

## Reports & Artifacts

- **HTML Report**: `reports/home_page_report.html` (self-contained with failure screenshots embedded).
- **Screenshots**: Saved to `screenshots/` on failure or key verification steps.
- **Execution Logs**: Written to `logs/automation.log` and displayed in the terminal console.
