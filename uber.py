import pandas as pd
import numpy as np

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
    (uber_data["payment_type"] != 0)
]

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
    4: "Nassau or Westchester",
    5: "Negotiated fare",
    6: "Group ride"
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

# Creating trip table
trip = uber_data.drop(columns=["store_and_fwd_flag", "improvement_surcharge", "airport_fee", "total_amount"])

trip = trip.merge(ratecode_data[["ratecode_id", "ratecode_num"]], left_on="RatecodeID", right_on="ratecode_num", how="inner")
trip = trip.merge(payment_type_data[["payment_type_id", "payment_type_num"]], left_on="payment_type", right_on="payment_type_num", how="inner")
trip = trip.merge(vendor_data[["vendor_id", "vendor_num"]], left_on="VendorID", right_on="vendor_num", how="inner")

trip.drop(columns=["VendorID", "RatecodeID", "payment_type", "ratecode_num", "payment_type_num", "vendor_num"], inplace=True)

trip.rename(
    columns={
        "tpep_pickup_datetime": "pickup_datetime",
        "tpep_dropoff_datetime": "dropoff_datetime",
        "PULocationID": "pulocation_id",
        "DOLocationID": "dolocation_id",
        "extra": "extra_amount"
    }, 
    inplace=True)

trip["store_and_fwd_flag"] = uber_data["store_and_fwd_flag"].apply(lambda x: True if x == "Y" else False)
trip["improvement_surcharge"] = uber_data["improvement_surcharge"].apply(lambda x: True if x == 0.3 else False)
trip["airport_fee"] = uber_data["airport_fee"].apply(lambda x: True if x == 1.25 else False)

trip["total_amount"] = trip[["fare_amount", "extra_amount", "mta_tax", "tip_amount", "tolls_amount", "congestion_surcharge"]].sum(axis=1)
trip["total_amount"] = np.where(trip["airport_fee"], trip["total_amount"] + 1.25, trip["total_amount"])
trip["total_amount"] = np.where(trip["improvement_surcharge"], trip["total_amount"] + 0.3, trip["total_amount"])

trip["pickup_datetime"] = pd.to_datetime(trip["pickup_datetime"])
trip["dropoff_datetime"] = pd.to_datetime(trip["dropoff_datetime"])

trip["store_and_fwd_flag"] = trip["store_and_fwd_flag"].astype(bool)
trip["improvement_surcharge"] = trip["improvement_surcharge"].astype(bool)
trip["airport_fee"] = trip["airport_fee"].astype(bool)

trip = trip[trip["fare_amount"] > 0]
trip = trip[trip["total_amount"] > 0]

trip["trip_id"] = trip.index + 1

trip = trip[[
    "trip_id",
    "vendor_id", 
    "pickup_datetime", 
    "dropoff_datetime", 
    "pulocation_id", 
    "dolocation_id", 
    "passenger_count", 
    "trip_distance",
    "ratecode_id",
    "payment_type_id",
    "store_and_fwd_flag",
    "fare_amount",
    "extra_amount",
    "mta_tax",
    "improvement_surcharge",
    "tip_amount",
    "tolls_amount",
    "congestion_surcharge",
    "airport_fee",
    "total_amount"
]]