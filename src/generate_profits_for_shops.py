import csv
from gen_product import generate_profit_for_one_shop

lines = []
# Open the CSV file
with open('merged_data.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    
    # Iterate over each row, where each row is a dictionary
    for row in csv_reader:
        lines.append(
            {
                "id": row[""],
                "sales": generate_profit_for_one_shop(row)
            }
        )

with open("sales.csv", 'w', encoding="utf-8") as fh:
    fieldnames = ["id", "sales"]
    csv_writer = csv.DictWriter(fh, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(lines)
