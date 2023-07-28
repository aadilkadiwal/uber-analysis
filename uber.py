import pandas as pd

# To read uber_data.csv file and convert into DataFrame
uber_data = pd.read_parquet("uber_data.parquet")

# To read location_zone.csv file and convert into DataFrame
location_data = pd.read_csv("location_zone.csv")

# Creating location table
location_data["LocationID"] = location_data[["LocationID"]].drop_duplicates().reset_index(drop=True)
location_data.rename(columns={"LocationID": "location_id", "Borough": "borough", "Zone": "zone"}, inplace=True)

# Cleaning data

# Removing null or NaN value from RatecodeID and payment_type columns
uber_data.dropna(subset=["RatecodeID", "payment_type"], inplace=True)

# Converting RatecodeID columns datatype from float to int
uber_data["RatecodeID"] = uber_data["RatecodeID"].astype(int)

# Removing 6 and 99 value from RatecodeID and 0 value from payment_type column
uber_data = uber_data[
    (uber_data["RatecodeID"] != 6) & 
    (uber_data["RatecodeID"] != 99) & 
    (uber_data["payemnt_type"] != 0)
]

# Removing 

# Creating vendor table
vendor_type = {
    1: " Creative Mobile Technologies, LLC",
    2: "VeriFone Inc.",
    5: "Gett",
    6: "Ingogo"
}
vendor_data = uber_data[["VendorID"]].drop_duplicates().reset_index(drop=True)
vendor_data["vendor_id"] = vendor_data.index + 1
vendor_data["vendor_name"] = vendor_data["VendorID"].map(vendor_type)
vendor_data.rename(columns={"VendorID": "vendor_num"}, inplace=True)
vendor_data = vendor_data[["vendor_id", "vendor_num", "vendor_name"]]

# Creating ratecode table
ratecode_type = {
    1: "Standard rate",
    2: "JFK",
    3: "Newark",
    4: "Negotiated fare",
    5: "Group ride"
}
ratecode_data = uber_data[["RatecodeID"]].drop_duplicates().reset_index(drop=True)
ratecode_data["ratecode_id"] = ratecode_data.index + 1
ratecode_data["ratecode_name"] = ratecode_data["RatecodeID"].map(ratecode_type)
ratecode_data.rename(columns={"RatecodeID": "ratecode_num"}, inplace=True)
ratecode_data = ratecode_data[["ratecode_id", "ratecode_num", "ratecode_name"]]

# Creating payment_type table
payment_type = {
    1: "Credit card",
    2: "Cash",
    3: "No charge",
    4: "Dispute",
    5: "Unknown",
    6: "Voided trip"
}
payment_type_data = uber_data[["payment_type"]].drop_duplicates().reset_index(drop=True)
payment_type_data["payment_type_id"] = payment_type_data.index + 1
payment_type_data["payment_type_name"] = payment_type_data["payment_type"].map(payment_type)
payment_type_data.rename(columns={"payment_type": "payment_type_num"}, inplace=True)
payment_type_data = payment_type_data[["payment_type_id", "payment_type_num", "payment_type_name"]]