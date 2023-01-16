from pony.orm import *

db = Database()
db.bind(provider="sqlite", filename="db.sqlite", create_db=True)
sql_debug(True)


class Waifu(db.Entity):
    waifu_id = PrimaryKey(int, auto=True)
    anilist_id = Required(str)
    full_name = Required(str, unique=True)
    gender = Required(str)
    age = Required(str, default="Unknown")
    image_url = Required(str)
    source_title = Required(str)
    captured = Required(bool, default=False)
    value = Required(int)


db.generate_mapping(create_tables=True)


@db_session
def add_waifu(name, gender, age, image, source, value, anilist_id):
    Waifu(
        full_name=name,
        gender=gender,
        age=age,
        image_url=image,
        source_title=source,
        value=value,
        anilist_id=anilist_id,
    )
