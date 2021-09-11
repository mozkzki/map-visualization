from main.my.map import Map
from main.my.places import Places


def main():
    name = input("place name: 東京")
    info = input("place info: 電波塔")

    places = Places()
    places.load("places_test.db")

    # 全取得
    # places.select_all()
    # 名前でフィルタ
    places.filter({"name": name})
    # 情報欄でフィルタ
    places.filter({"info": info})

    places.geocoding()

    map = Map()
    map.save(places.list, "map.html")


if __name__ == "__main__":
    main()
