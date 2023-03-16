# ScanURL

ScanURL is a web-based tool that can be used for OSINT (Open Source Intelligence) purposes. The tool retrieves various pieces of information about a URL or a first level domain. The information retrieved includes WHOIS, IP, reverse DNS and redirections analysis.

## How it works

To use the tool, simply paste the URL or first level domain into the input field and click on the "Scan" button. The tool will retrieve the relevant information and display it in a clear and concise way.

## Why is ScanURL relevant for OSINT?

ScanURL is a powerful tool for OSINT because it allows you to quickly and easily gather information about a website or domain. This information can be used to help identify potential threats or to gather intelligence about a particular target. By using ScanURL, you can save time and streamline your OSINT workflow.

## How to use it locally?

### Install pipenv
`pip install pipenv`

### Install dependencies
`pipenv install`

### Activate virtual environment
`pipenv shell`

### Run the application
`pipenv run uvicorn main:app --reload`

### View the API endpoints
Redoc: http://localhost:8000/redoc

