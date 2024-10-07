from config import DATA_PATH, DISTANCEMATRIX_URL, DISTANCEMATRIX_API_KEY
import pandas as pd
import requests


class DatasetProcessor:
    DISTANCE_URL = DISTANCEMATRIX_URL

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
        """This method WOULD return the distance/estimated travel time data
        from a routing API such as distancematrix.ai or Google Maps if one was available

        Args:
            booking (pd.Series | NamedTuple): A single booking record

        Returns:
            dict: a dictionary of distance/time values.
        """
        collection_lat = booking["FIRST_COLLECTION_LATITUDE"]
        collection_lon = booking["FIRST_COLLECTION_LONGITUDE"]
        delivery_lat = booking["LAST_DELIVERY_LATITUDE"]
        delivery_lon = booking["LAST_DELIVERY_LATITUDE"]
        return requests.get(
            f"{self.DISTANCE_URL}?lat1={collection_lat}&lon1={collection_lon}&lat2={delivery_lat}&lon2={delivery_lon}&key={DISTANCEMATRIX_API_KEY}"
        )

    def transform(self, df):
        pass

    def clean(self, df):
        pass

    def process(self, df_shipping, df_gps):
        df = self.merge_data(df_shipping, df_gps)
        df = self.transform(df)
        df = self.clean(df)
