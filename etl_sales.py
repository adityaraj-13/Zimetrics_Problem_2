import pandas as pd
import os

INPUT_FILE = 'sales.csv'
OUTPUT_FILE = 'clean_sales.json'
# Starting ETL process
def run_etl():
    print("Starting ETL process...\n")
    try:
        if not os.path.exists(INPUT_FILE):
            raise FileNotFoundError(f"Input file {INPUT_FILE} does not exist.")
        #Load data
        df = pd.read_csv(INPUT_FILE, header=None, names=["ID", "Product", "Price", "Country"], skipinitialspace=True)
        print("Data loaded successfully.\n")

        # Clean data 
        print("****************************************\n")
        #1.Remove $ sign from Price and convert to float 
        df['Price'] = df['Price'].replace(r'[\$,]', '', regex=True).astype(float)
        print("Price column cleaned. \n")

        #2. Remove double quotes from Product names
        df['Product'] = df['Product'].astype(str).str.replace('"', '').str.strip()
        print("Product column cleaned. \n")

        #3. Remove duplicate records
        df.drop_duplicates(inplace=True, subset=['Product', 'Price'])
        print("Duplicate records removed.\n")

        #4. Price conversion from USD to INR (1 USD = 83 INR)
        df['Price'] = df['Price'] * 83
        print("Price converted from USD to INR. \n")

        print("****************************************\n")

        #5. Save the cleaned data to JSON
        df.to_json(OUTPUT_FILE, orient='records', indent=4)
        print(f"Cleaned data saved to {OUTPUT_FILE}.")
    except Exception as e:
        print(f"ETL process failed: {e}")
        raise

if __name__ == "__main__":
    run_etl()