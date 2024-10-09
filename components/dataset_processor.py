from config import DISTANCEMATRIX_URL, DISTANCEMATRIX_API_KEY
from geopy.distance import geodesic
from dateutil.relativedelta import relativedelta
import pandas as pd
import requests


class DatasetProcessor:
    """Contains the methods for processing the raw data into a feature store that can be used for model
    training"""

    DISTANCE_API_URL = DISTANCEMATRIX_URL

    @staticmethod
    def merge_data(shipment_bookings, gps_data):
        latest_gps = gps_data.sort_values(
            by="RECORD_TIMESTAMP", ascending=False
        ).drop_duplicates(
            subset=["SHIPMENT_NUMBER"],
            keep="first",
        )
        shipment_bookings = shipment_bookings.merge(
            latest_gps[["SHIPMENT_NUMBER", "RECORD_TIMESTAMP"]].rename(
                {"RECORD_TIMESTAMP": "LATEST_GPS_TIMESTAMP"}, axis=1
            ),
            on="SHIPMENT_NUMBER",
            how="left",
        )
        return shipment_bookings

    def get_route_info(self, booking):
        """This method *would* return the distance/estimated travel time data
        from a routing API such as distancematrix.ai or Google Maps if one was available

        Args:
            booking (pd.Series | NamedTuple): A single booking record

        Returns:
            dict: a dictionary of distance/time values.
        """
        params = {
            "lat1": booking["FIRST_COLLECTION_LATITUDE"],
            "lon1": booking["FIRST_COLLECTION_LONGITUDE"],
            "lat2": booking["LAST_DELIVERY_LATITUDE"],
            "lon2": booking["LAST_DELIVERY_LONGITUDE"],
            "key": DISTANCEMATRIX_API_KEY,
        }
        response = requests.get(f"{self.DISTANCE_API_URL}", params=params)
        return {
            "distance": response.json()["info"]["distance"],
            "duration": response.json()["info"]["duration"],
        }

    def transform(self, df):
        """Carries out transformations that cannot easily be carried out in the training pipeline.

        Args:
            df (pd.DataFrame): The DataFrame to be transformed
        """
        # Retrieve disatnce and duration from the API when available
        # df["DURATION"] = df.apply(lambda x: self.get_route_info(x)["duration"], axis=1)
        # df["DISTANCE"] = df.apply(lambda x: self.get_route_info(x)["distance"], axis=1)

        # Substitute distance with geodesic distance
        df["DISTANCE"] = geodesic(
            df["FIRST_COLLECTION_LATITUDE"],
            df["FIRST_COLLECTION_LONGITUDE"],
            df["LAST_DELIVERY_LATITUDE"],
            df["LAST_DELIVERY_LONGITUDE"],
        ).km

        df["SHIPMENT_DURATION"] = (
            df["LAST_DELIVERY_SCHEDULE_LATEST"]
            - df["FIRST_COLLECTION_SCHEDULE_EARLIEST"]
        ).apply(lambda x: x.total_seconds() / 3600)

        return df

    def clean(self, df):
        """Performs cleaning operations on the DataFrame df.

        Args:
            df (pd.DataFrame): The DataFrame to be cleaned.
        """
        pass

    def process(self, df_shipping, df_gps):
        df = self.merge_data(df_shipping, df_gps)
        df = self.transform(df)
        df = self.clean(df)
        return df
