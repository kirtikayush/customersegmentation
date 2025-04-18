import pandas as pd

file_path = 'data.csv'  # Replace with your path
df = pd.read_csv(file_path, encoding='ISO-8859-1')

# Drop rows with missing CustomerID
df.dropna(subset=['CustomerID'], inplace=True)

# Remove cancelled orders (InvoiceNo starting with 'C')
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]

# Create TotalPrice column
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# Convert InvoiceDate to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Save cleaned data
df.to_csv('cleaned_data.csv', index=False)
