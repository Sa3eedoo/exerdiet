import pandas as pd

# Read the CSV file
data = pd.read_csv('modified_food.csv')

# Specify your column name
column_name = 'name'

# Remove single quotes from the specified column
data[column_name] = data[column_name].str.replace("'", "")
data[column_name] = data[column_name].str.replace("\"", "")

# Specify your MySQL table name
table_name = 'diet_food'

# Generate the MySQL script
script = ''
for index, row in data.iterrows():
    values = row.values.tolist()
    values[0] = f'"{values[0]}"' if pd.notnull(values[0]) else 'NULL'
    values[1] = f'"{values[1]}"' if pd.notnull(values[0]) else 'NULL'
    columns_str = ', '.join(data.columns)
    values_str = ', '.join(str(value) if pd.notnull(
        value) else 'NULL' for value in values)
    script += f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});\n"

# Save the script to a file
with open('food.sql', 'w') as file:
    file.write(script)
