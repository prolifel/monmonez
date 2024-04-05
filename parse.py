def parse_bank_statement(text):
    """
    Parses a text file containing a bank statement with data on each line and returns a list of dictionaries,
    where each dictionary represents a transaction with the following keys:
      - date: Transaction date (if present)
      - description: Transaction description
      - out: Amount spent (negative value) or None if income
      - in: Amount received (positive value) or None if expense
      - balance: Account balance after the transaction (if present)
    """
    transactions = []
    for line in text.splitlines():
        data = line.strip().split(" ")
        # Description starts from index 1
        transaction = {"description": " ".join(data[1:])}

        # Identify transaction based on presence of specific words
        if "OVERBOOKING" in data or "BILL PAYMENT" in data or "PAY" in data:
            # Description is the first word for these types
            transaction["description"] = data[0]
            if len(data) > 3:
                # Assuming negative amount in third position
                transaction["out"] = -float(data[2])
                # Assuming positive amount in fourth position
                transaction["in"] = float(data[3])
        # Check for negative amount in second position
        elif len(data) > 4 and "-" in data[1]:
            transaction["date"] = data[0]
            # Extract negative amount
            transaction["out"] = -float(data[1].replace("-", ""))
            transaction["in"] = float(data[2])
            transaction["balance"] = float(data[4])
        elif len(data) > 4:
            transaction["date"] = data[0]
            transaction["in"] = float(data[1])
            transaction["balance"] = float(data[4])

        transactions.append(transaction)
    return transactions


# Read the text file content
with open("out.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Parse the text and get transactions
transactions = parse_bank_statement(text)

# Print the first 4 transactions
for i in range(4):
    print(transactions[i])
