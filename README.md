## Personal Budgeting App
A personal budgeting app designed to track monthly transactions and provide a financial summary.

## Current Features
- **/Transactions/import:** Import from Capital One checking and savings accounts and credit cards. Duplicates are allowed within an import file, but transactions already in the database are not imported again.
- **/Transactions:** Retrieve all transactions
- **/transactions/period:** Retrieve transactions that are within the year and month provided (YYYY-MM)

## Tech Stack
- Python
- Flask
- SQlite
- JSON
- Git

## Task Commands
- **Build:** python -m backend.main build
- **Format Code:** python -m backend.main spotlessApply
- **Run Server:** python -m backend.main runServer

## Run Tests
- **Run all Tests:** python -m pytest
- **Run all tests in a specific file:** python -m pytest test_path -v -s
- **Run a specific test method:** python -m pytest test_path::test_method -v -s
