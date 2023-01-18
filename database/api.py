import requests
from time import sleep
from pprint import pprint
from models import *
from model_logic import *

url = "https://graphql.anilist.co"
query = """
        query ($id: Int) {
  Character (id: $id) {
    id
    name {
      full
    }
    gender
    age
    image {
      large
    }
    media {
      nodes {
        title {
          english
          romaji
        }
      }
      edges {
        characterRole
      }
    }
  }
}
"""

VALUE = {"MAIN": 500, "SUPPORTING": 250, "BACKGROUND": 100}

for char_id in range(95060, 140000):
    sleep(0.7)
    variables = {"id": char_id}
    response = requests.post(url, json={"query": query, "variables": variables})
    match response.status_code:
        case 404:
            print(f"{char_id} not found")
        case 200:
            response = response.json()["data"]["Character"]
            gender = response["gender"]
            if gender == "Male":
                print(f"Skipped {response['id']}: - Male")
            elif gender == "Female":
                anilist_id = response["id"]
                name = response["name"]["full"]
                gender = response["gender"]
                age = response["age"]
                source_title = response["media"]["nodes"][0]["title"]["english"]
                romaji = response["media"]["nodes"][0]["title"]["romaji"]
                image_url = response["image"]["large"]
                role = response["media"]["edges"][0]["characterRole"]
                value = VALUE[role]
                if age == None:
                    age = "Unknown"
                if source_title == None:
                    source_title = romaji
                if image_url != None and not waifu_exists_by_anilist_id(anilist_id):
                    waifu = add_waifu(
                        name, gender, age, image_url, source_title, value, anilist_id
                    )
                    print(f"Added {anilist_id}: {name} from {source_title}")
                else:
                    pass
        case _:
            pass
