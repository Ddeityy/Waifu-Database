import requests
from time import sleep
from pprint import pprint
from pony_db import *

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
      medium
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

for char_id in range(1, 140000):
    sleep(1.5)
    variables = {"id": char_id}
    response = requests.post(url, json={"query": query, "variables": variables})
    match response.status_code:
        case 404:
            pass
        case 200:
            response = response.json()["data"]["Character"]
            gender = response["gender"]
            if gender == "Female":
                anilist_id = response["id"]
                name = response["name"]["full"]
                gender = response["gender"]
                age = response["age"]
                source_title = response["media"]["nodes"][0]["title"]["english"]
                romaji = response["media"]["nodes"][0]["title"]["romaji"]
                image_url = response["image"]["medium"]
                role = response["media"]["edges"][0]["characterRole"]
                value = VALUE[role]
                if age == None:
                    age = "Unknown"
                if source_title == None:
                    source_title = romaji
                if image_url != None:
                    add_waifu(
                        name, gender, age, image_url, source_title, value, anilist_id
                    )
                    print(f"Added {name} from {source_title}")
                else:
                    pass
        case _:
            pass
