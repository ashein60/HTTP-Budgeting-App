from transactions.transaction import Transaction

def import_checking_saving_account(reader, connection):
    for row in reader:
        transaction = Transaction.from_checking_and_saving_account_csv_row(row)
        insert_transaction(connection, transaction)

def import_credit_card_account(reader, connection):
    for row in reader:
        transaction = Transaction.from_checking_and_saving_account_csv_row(row)
        insert_transaction(connection, transaction)

def insert_transaction(connection, transaction):
    connection.execute(
        "INSERT INTO transactions (date, account, description, category, debit, credit) VALUES (?, ?, ?, ?, ?, ?)",
        (
            transaction.date,
            transaction.account,
            transaction.description,
            transaction.category,
            transaction.debit,
            transaction.credit
        )
    )