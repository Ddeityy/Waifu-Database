from pony.orm import *

db = Database()
db.bind(provider="sqlite", filename="db.sqlite", create_db=True)
sql_debug(True)


class User(db.Entity):
    discord_id = PrimaryKey(int)
    name = Required(str, unique=True)


class Waifu(db.Entity):
    waifu_id = PrimaryKey(int, auto=True)
    anilist_id = Required(int, unique=True)
    full_name = Required(str)
    gender = Required(str)
    age = Required(str, default="Unknown")
    image_url = Required(str)
    source_title = Required(str)
    captured = Required(bool, default=False)
    value = Required(int)


db.generate_mapping(create_tables=True)
