from config import DATA_PATH
from components import FeatureProcessor
import pandas as pd


def read_data():
    """Reads the CSV file"""
    shipping_date_cols = [
        "FIRST_COLLECTION_SCHEDULE_EARLIEST",
        "FIRST_COLLECTION_SCHEDULE_LATEST",
        "LAST_DELIVERY_SCHEDULE_EARLIEST",
        "LAST_DELIVERY_SCHEDULE_LATEST",
    ]
    gps_date_cols = ["TIMESTAMP"]
    return (
        pd.read_csv(
            f"{DATA_PATH}/Shipment_bookings.csv", parse_dates=[shipping_date_cols]
        ),
        pd.read_csv(f"{DATA_PATH}/GPS_data.csv", parse_dates=[gps_date_cols]),
    )


def process_data(shipment_bookings, gps):
    fp = FeatureProcessor()
    df = fp.process(shipment_bookings, gps)
    return df


if __name__ == "__main__":
    bookings_data, gps_data = read_data()
    data_processed = process_data(bookings_data, gps_data)
    data_processed.to_csv("training_data.csv", index=False)
