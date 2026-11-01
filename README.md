## Personal Budgeting App
A personal budgeting app designed to track monthly transactions and provide a financial summary. 

## Basic Structure
- **Transactions:** id (PK), date, account, description, category, debit, credit
- **Category Groups:** name (PK), actual total, expected total
- **Categories:** name (PK), group name (FK), actual, expected

## Getting Started
- From the command line, please run the following: **python -m backend.main build createSeedData startServer**
- This will create your database with seed data and start a local server for you.
- For now, please use an API testing tool or python to run HTTP requests. I've been using python by importing requests.

## Current Features
- **/transasctions:** Manage transactions with import, get all, and get by period (YYYY-MM)
- **/category_group:** Manage category groups, such as "Income" or "Savings," with add by name, delete by name, and get all
- **/category:** Manage categories, such as "Rent" or "Groceries," with add by name, delete by name, and get all

## Todo
- **Update Category Groups & Categories:** to contain totals and for categories to be unique per period (YYYY-MM)
- **Account Alias:** Account numbers are a bit hard to track, so I'll add an alt name
- **Transaction Import Rules:** Restrict what data is imported and assign categories and category groups based on the description
- **Authentication:** Since this is a small project, I'll just manage one database with one username and password
- **UI:** Will likely just be a console program, but I use react eventually

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
