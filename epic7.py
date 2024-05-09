import html_to_json
from urllib.request import urlopen
import json


base_url = "https://epic7db.com/heroes"
output_file = "epic7_characters.txt"

def get_character_info(character_info : dict) -> None:
    url = base_url+"/"+character_info['name'].replace(' ', '-').replace('\'','').replace('&',"and").replace(".","").lower()
    print(url)
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    file = html_to_json.convert(html)
    character_info["img"] = file["html"][0]["head"][0]["link"][2]["link"][0]["meta"][0]["_attributes"]["content"]

def get_character_list(json) -> list[dict[str, str]]:
    character_list = []
    for character_div in json["html"][0]["body"][0]["div"][0]["div"][0]["ul"][0]["li"]:
        character_info = {}
        character_info["name"] = character_div["a"][0]["_value"]
        character_list.append(character_info)
    return character_list

def main() -> None:
    page = urlopen(base_url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    file = html_to_json.convert(html)       
    result = get_character_list(file)
    output = []
    for character in result:
        get_character_info(character)
        output.append(f'{character["name"]}--Epic 7--{character["img"]}')
    with open(output_file, 'w') as f:
        for item in output:
            f.write("%s\n" % item)

if __name__ == "__main__":
    main()
