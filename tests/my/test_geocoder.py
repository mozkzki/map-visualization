from main.my.geocoder import Geocoder


class TestGeocoder:
    def test_method(self) -> None:
        g = Geocoder()
        lat, lng = g.get("東京タワー")
        assert lat == "35.658581"
        assert lng == "139.745433"
