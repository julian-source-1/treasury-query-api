import requests
import pandas as pd

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
        df.to_csv(filename, index=False)
        print(f"Data successfully saved to {filename}")
    else:
        print("No data available to save")

# Example usage
start_year = 2022
current_year = 2023  # Update this as needed
field = "bid_to_cover_ratio"
data = get_treasury_data(start_year, current_year, field)

# Call the save_data_to_csv function without needing to pass a filename
save_data_to_csv(data, start_year, current_year)

