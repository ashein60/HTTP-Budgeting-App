## Personal Budgeting App
A personal budgeting app designed to track monthly transactions and provide a financial summary.

## Current Features
- **/transasctions:** Manage transactions with import, get all, and get by period (YYYY-MM)
- **/category_group:** Manage category groups, such as "Income" or "Savings," with add by name, delete by name, and get all
- **/category:** Manage categories, such as "Rent" or "Groceries," with add by name, delete by name, and get all

## Planned Features
- **Transaction Import Rules:** Restrict what data is imported and assign categories and category groups based on the description
- **Summary Table and APIs:** Crucial for this software to be useful
- **UI:** Will likely be made with React. Progress wont start until the MVP is finished. 

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
