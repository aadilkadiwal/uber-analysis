import pandas as pd

# To read uber_data.csv file and convert into DataFrame
data = pd.read_csv("uber_data.csv")

# To read location_zone.csv file and convert into DataFrame
location_data = pd.read_csv("location_zone.csv")

# Creating location table
location_data["LocationID"] = location_data[["LocationID"]].drop_duplicates().reset_index(drop=True)
location_data.rename(columns={"LocationID": "location_id", "Borough": "borough", "Zone": "zone"}, inplace=True)

# Creating vendor table
vendor_type = {
    1: " Creative Mobile Technologies, LLC",
    2: "VeriFone Inc.",
    5: "Gett",
    6: "Ingogo"
}
vendor = data[["VendorID"]].drop_duplicates().reset_index(drop=True)
vendor["vendor_id"] = vendor.index
vendor["vendor_name"] = vendor["VendorID"].map(vendor_type)
vendor.rename(columns={"VendorID": "vendor_num"}, inplace=True)
vendor = vendor[["vendor_id", "vendor_num", "vendor_name"]]