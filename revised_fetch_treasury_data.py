
import requests
import pandas as pd
import os

# Define the subdirectory path
subdirectory = 'fetched-data'

# Check if the subdirectory exists, and if not, create it
if not os.path.exists(subdirectory):
    os.makedirs(subdirectory)

def get_treasury_data(year, field):
    base_url = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"
    endpoint = "v1/accounting/od/auctions_query"  # Replace with the actual endpoint
    
    params = {
        "filter": f"issue_date:gte:{year}-01-01,issue_date:lte:{year}-12-31",
        "page[size]": 1000,  # Adjust according to the API's limits
        "format": "json"
    }
    
    response = requests.get(base_url + endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data:", response.status_code)
        return None

def collect_and_save_data(start_year, end_year, field):
    all_data_frames = []
    for year in range(start_year, end_year + 1):
        data = get_treasury_data(year, field)
        if data and 'data' in data:
            df = pd.DataFrame(data['data'])
            all_data_frames.append(df)
            print(f"Data for {year} fetched and processed.")
        else:
            print(f"No data available for {year}")
    
    # Combine all data into a single DataFrame and save to CSV
    if all_data_frames:
        combined_df = pd.concat(all_data_frames, ignore_index=True)
        combined_file_path = os.path.join(subdirectory, "combined_treasury_data.csv")
        combined_df.to_csv(combined_file_path, index=False)
        print(f"All data combined into {combined_file_path}")

# Example usage
field = "bid_to_cover_ratio"  # Field to fetch, adjust as needed
start_year = 2010
end_year = 2020

collect_and_save_data(start_year, end_year, field)
