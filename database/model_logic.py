from pony.orm import *
from .models import *

db = Database()
db.bind(provider="sqlite", filename="db.sqlite", create_db=True)
sql_debug(False)


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


@db_session
def waifu_exists_by_anilist_id(ani_id):
    return Waifu.exists(anilist_id=ani_id)


@db_session
def get_random_waifu(waifu_id):
    return Waifu.get(waifu_id=waifu_id)
