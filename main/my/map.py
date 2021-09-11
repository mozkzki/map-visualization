import folium
import pandas as pd


class Map:
    def save(self, places_list: list, output_path: str = "map.html"):
        restaurant_list = []
        latitude_list = []
        longtude_list = []

        for place in places_list:
            name = place[1]
            # info = place[2]
            # address = place[3]
            lat = place[4]
            lng = place[5]
            link = place[6]

            try:
                float(lat)
            except ValueError:
                continue

            try:
                float(lng)
            except ValueError:
                continue

            restaurant_list.append("<a href='{}'>{}</a>".format(link, name))
            latitude_list.append(float(lat))
            longtude_list.append(float(lng))

        restaurants = pd.DataFrame(
            {
                "restaurant": restaurant_list,
                "latitude": latitude_list,
                "longtude": longtude_list,
            }
        )

        map = folium.Map(location=[35.736489, 139.746875], zoom_start=5)
        for i, r in restaurants.iterrows():
            folium.Marker(
                location=[r["latitude"], r["longtude"]], popup=r["restaurant"]
            ).add_to(map)

        map.save(output_path)
