from pony.orm import *
from .models import *
from random import randint

db = Database()
db.bind(provider="sqlite", filename="db_danbooru_incomplete.sqlite", create_db=True)
sql_debug(False)


@db_session
def get_random_waifu():
    waifu_range = count(w for w in Waifu if w.post_count > 1)
    waifu_id = randint(1, waifu_range)
    return Waifu.get(id=waifu_id)
