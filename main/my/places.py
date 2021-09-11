import sqlite3
import time
from typing import Dict

from main.my.geocoder import Geocoder
from tqdm import tqdm


# 場所データ保持クラス
class Places:
    def __init__(self):
        self.__db: sqlite3.Connection = None
        self.__cursor: sqlite3.Cursor = None
        self.__list: list = []

    def __del__(self):
        if self.__db:
            self.__db.close()

    def load(self, db_file_path: str):
        # 指定のDBファイルを読み込む
        self.__db = sqlite3.connect(db_file_path)
        self.__cursor = self.__db.cursor()
        self.__cursor = self.__cursor.execute(
            "CREATE TABLE IF NOT EXISTS places(\
                id INTEGER PRIMARY KEY AUTOINCREMENT, \
                name TEXT UNIQUE NOT NULL, \
                info TEXT NOT NULL, \
                address TEXT NOT NULL, \
                lat TEXT, \
                lng TEXT, \
                link TEXT NOT NULL \
            );"
        )

    @property
    def list(self) -> list:
        return self.__list

    def select_all(self) -> None:
        self.__list = self.__cursor.execute("SELECT * FROM places").fetchall()

    def filter(self, params: Dict) -> None:
        self.__list = self.__cursor.execute(
            self.__get_sql(),
            self.__get_sql_parameter(params),
        ).fetchall()

    def fetchone(self, params: Dict) -> Dict:
        place = self.__cursor.execute(
            self.__get_sql(),
            self.__get_sql_parameter(params),
        ).fetchone()
        return {
            "name": place[1],
            "info": place[2],
            "address": place[3],
            "lat": place[4],
            "lng": place[5],
            "link": place[6],
        }

    def is_exist(self, params: Dict) -> bool:
        cursor = self.__db.execute(
            self.__get_sql(),
            self.__get_sql_parameter(params),
        )
        if cursor.fetchone():
            return True
        else:
            return False

    def __get_sql(self):
        return "SELECT * FROM places WHERE name LIKE ? AND info LIKE ?"

    def __get_sql_parameter(self, params: Dict):
        return (
            "%" + params.get("name", "") + "%",
            "%" + params.get("info", "") + "%",
        )

    def add(self, place: tuple):
        self.__db.execute(
            "INSERT INTO places (name, info, address, lat, lng, link) "
            + "VALUES (?, ?, ?, ?, ?, ?)"
            + "ON CONFLICT (name)"
            + "DO UPDATE SET "
            + "  info = excluded.info,"
            + "  address = excluded.address,"
            + "  lat = excluded.lat,"
            + "  lng = excluded.lng,"
            + "  link = excluded.link",
            (
                # place[0]はid
                place[1],
                place[2],
                place[3],
                place[4],
                place[5],
                place[6],
            ),
        )
        self.__db.commit()

    def geocoding(self, is_db_update: bool = False) -> None:
        new_list: list = []
        first = True
        for place in tqdm(self.list):
            if not first:
                # 負荷をかけ過ぎない用に
                time.sleep(10)
            first = False

            id = place[0]
            name = place[1]
            info = place[2]
            address = place[3]
            # lat": place[4]
            # lng": place[5]
            link = place[6]

            geocoder = Geocoder()
            lat, lng = geocoder.get(address)

            new = (
                id,
                name,
                info,
                address,
                lat,
                lng,
                link,
            )
            print("* {} ({}) -----> ({}, {})".format(name, address, lat, lng))

            if is_db_update:
                self.add(new)

            new_list.append(new)

        self.__list = new_list
