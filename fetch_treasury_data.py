import requests
import pandas as pd
import os

# Define the subdirectory path
subdirectory = 'fetched-data'

# Check if the subdirectory exists, and if not, create it
if not os.path.exists(subdirectory):
    os.makedirs(subdirectory)

def get_treasury_data(start_year, end_year, field):
    base_url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"
    endpoint = "v1/accounting/od/auctions_query"  # Replace with the actual endpoint
    
    params = {
        "filter": f"issue_date:gte:{start_year},issue_date:lte:{end_year}",
        "page[size]": 1000,  # Adjust according to the API's limits
        "format": "json"
    }
    
    response = requests.get(base_url + endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data:", response.status_code)
        return None

def save_data_to_csv(data, start_year, current_year):
    if data and 'data' in data:
        df = pd.DataFrame(data['data'])
        # Construct filename with start_year and current_year included
        filename = f"treasury_data_{start_year}_to_{current_year}.csv"
        # Update file path to include the subdirectory
        file_path = os.path.join(subdirectory, filename)
        df.to_csv(file_path, index=False)
        print(f"Data successfully saved to {file_path}")
    else:
        print("No data available to save")

# Example usage
start_year = 2023
current_year = 2024  # Update this as needed
field = "bid_to_cover_ratio"
data = get_treasury_data(start_year, current_year, field)

# Call the save_data_to_csv function without needing to pass a filename
save_data_to_csv(data, start_year, current_year)

