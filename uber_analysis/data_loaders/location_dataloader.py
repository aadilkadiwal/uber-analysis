import io
import pandas as pd
from google.cloud import storage

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here

    storage_client = storage.Client.from_service_account_json('cloud-credentials.json')
    
    bucket = storage_client.get_bucket('uber_data_analytic_project')
    blob = bucket.blob('location_zone.csv')
    blob_response = blob.download_as_string()
    blob_response = blob_response.decode("utf-8")

    return pd.read_csv(io.StringIO(blob_response), sep=',')

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
