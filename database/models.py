from pony.orm import *

db = Database()
db.bind(provider="sqlite", filename="db.sqlite", create_db=True)
sql_debug(True)


class Waifu(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    source = Required(str)
    post_count = Required(int)
    best_safe_post_id = Required(int, default=0)
    best_safe_post_score = Required(int, default=0)
    best_safe_post_image = Required(str, default="None")
    best_unsafe_post_id = Required(int, default=0)
    best_unsafe_post_score = Required(int, default=0)
    best_unsafe_post_image = Required(str, default="None")
    value = Required(int, default=0)


db.generate_mapping(create_tables=True)
