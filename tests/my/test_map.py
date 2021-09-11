import os

import pytest
from main.my.map import Map
from main.my.places import Places


class TestMap:
    db_file_path = os.path.join(os.getcwd(), "./tests/resources/places.db")
    map_output_path = os.path.join(os.getcwd(), "./tests/map.html")
    map_output_path_with_filter = os.path.join(os.getcwd(), "./tests/map_filter.html")

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
        for i in range(1, 4):
            place = (
                "{}".format(i),
                "hoge-{}".format(i),
                "INFO-{}".format(i),
                "ADDRESS{}".format(i),
                "{}5.0".format(i),
                "1{}5.0".format(i),
                "https://www.google.co.jp",
            )
            places.add(place)

    def _tear_down(self):
        # DB削除
        os.remove(self.db_file_path)

    @pytest.fixture()
    def places(self):
        places = Places()
        places.load(self.db_file_path)
        return places

    def test_save(self, places: Places):
        places.select_all()
        map = Map()
        map.save(places.list, output_path=self.map_output_path)
