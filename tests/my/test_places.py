import os
from typing import Dict

import pytest
from main.my.places import Places


class TestPlaces:
    db_file_path = os.path.join(os.getcwd(), "./tests/resources/places.db")

    # テストメソッド前後に処理を行う
    @pytest.fixture(scope="function", autouse=True)
    def pre_function(self):
        scope = "Function"
        print(f"\n=== SETUP {scope} ===")
        self._setup()
        yield
        self._tear_down()
        print(f"\n=== TEARDOWN {scope} ===\n")

    def _setup(self):
        # 3箇所追加
        places = Places()
        places.load(self.db_file_path)
        for i in range(3):
            place = (
                "{}".format(i),
                "hoge-{}".format(i),
                "INFO-{}".format(i),
                "ADDRESS{}".format(i),
                "",
                "",
                "https://www.google.co.jp",
            )
            places.add(place)

    def _tear_down(self):
        # DB削除
        if os.path.exists(self.db_file_path):
            os.remove(self.db_file_path)

    @pytest.fixture()
    def places(self):
        places = Places()
        places.load(self.db_file_path)
        return places

    def test_is_exist_true(self, places: Places):
        assert places.is_exist({"name": "hoge-1"}) is True

    def test_is_exist_false(self, places: Places):
        assert places.is_exist({"name": "test"}) is False

    def test_add_存在しないアイテム(self, places: Places):
        assert places.is_exist({"name": "hoge-3"}) is False
        place = (
            "3",
            "hoge-3",
            "INFO-3",
            "ADDRESS3",
            "35.3",
            "130.3",
            "https://www.google.co.jp",
        )
        places.add(place)
        assert places.is_exist({"name": "hoge-3"}) is True

    def test_add_既存のアイテム(self, places: Places):
        assert places.is_exist({"name": "hoge-0"}) is True
        place = (
            "0",
            "hoge-0",
            "INFO-0",
            "ADDRESS0",
            "35.0",
            "130.0",
            "https://www.google.co.jp",
        )
        places.add(place)
        updated_place: Dict = places.fetchone({"name": "hoge-0"})
        assert updated_place.get("name") == "hoge-0"
        assert updated_place.get("info") == "INFO-0"
        assert updated_place.get("address") == "ADDRESS0"
        assert updated_place.get("lat") == "35.0"
        assert updated_place.get("lng") == "130.0"
        assert updated_place.get("link") == "https://www.google.co.jp"

    def test_fetchone(self, places: Places):
        place: Dict = places.fetchone({"name": "hoge-1"})
        assert place.get("name") == "hoge-1"
        assert place.get("info") == "INFO-1"
        assert place.get("address") == "ADDRESS1"
        assert place.get("lat") == ""
        assert place.get("lng") == ""
        assert place.get("link") == "https://www.google.co.jp"

    @pytest.mark.parametrize(
        "params",
        [
            ({"name": "hoge", "info": "INFO"}),
            ({"name": "hoge", "info": ""}),
            ({"name": "hoge"}),
            ({"name": "", "info": "INFO"}),
            ({"info": "INFO"}),
            ({}),
        ],
    )
    def test_filter(self, places: Places, params: Dict):
        places.filter(params)
        for i, place in enumerate(places.list):
            print(place[1])
            assert place[1] == "hoge-{}".format(i)
            assert place[2] == "INFO-{}".format(i)
        del places  # 明示的にデストラクタ呼び出し

    def test_select_all(self, places: Places):
        places.select_all()
        for place in places.list:
            name = place[1]
            info = place[2]
            address = place[3]
            lat = place[4]
            lng = place[5]
            link = place[6]
            print(
                """name    : {}
info    : {}
address : {}
lat     : {}
lng     : {}
link    : {}
-----------------------------""".format(
                    name, info, address, lat, lng, link
                )
            )

    @pytest.mark.slow
    def test_geocoding(self, places: Places):
        places.select_all()
        places.geocoding()
        actual = places.list
        print(actual)

    def test_create_data(self, places: Places):
        places.add(
            (
                "1",
                "東京タワー",
                "日本の東京都港区芝公園にある総合電波塔の愛称である。",
                "東京都港区芝公園４丁目２−８",
                "",
                "",
                "https://www.tokyotower.co.jp/",
            )
        )
        places.add(
            (
                "2",
                "東京スカイツリー",
                "東京都墨田区押上1-1-2にある電波塔であり、東武鉄道及び東武グループのシンボル的存在である。",
                "東京都墨田区押上１丁目１−２",
                "",
                "",
                "https://www.tokyo-skytree.jp/",
            )
        )
