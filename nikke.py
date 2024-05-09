from bs4 import BeautifulSoup
import requests
import html_to_json
from urllib.request import urlopen
import json 


base_url = "https://www.prydwen.gg/nikke/characters/"
output_file = "nikke_characters.txt"

def get_character_info(character_info : dict) -> None:
    print(character_info["name"])
    is_composed = True
    try :
        index = character_info["name"].index(":")
    except ValueError:
        is_composed = False
    if is_composed:
        if character_info["name"] in ["D: Killer Wife", "Ludmilla: Winter Owner", "Mica: Snow Buddy", "Privaty: Unkind Maid", "Scarlet: Black Shadow"]:
            character_url = character_info["name"].replace(":","").replace(" ","-").lower()
        elif character_info["name"] == "Helm: Aquamarine":
            character_url = "aqua-marine-helm"
        elif character_info["name"] == "Snow White: Innocent Days":
            character_url = "innocent-dayss-snow-white"
        else :
            raw_name = character_info["name"].split(":")
            affix = raw_name[1][1:].replace(" ", "-").lower()
            character_url = f'{affix}-{raw_name[0].lower()}'
    else:
        character_url = character_info["name"].lower().replace(" ", "-")
    url = base_url + character_url
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    file = html_to_json.convert(html)
    if character_info["name"] == "Snow White: Innocent Days":
        character_info["img"] = "https://www.prydwen.gg"+file['html'][0]["body"][0]["div"][0]["div"][0]["div"][0]["div"][1]["div"][1]["div"][1]["div"][1]["div"][1]["noscript"][0]["img"][0]["_attributes"]["srcset"].split(",")[2].split()[0]
    elif "picture" not in file['html'][0]["body"][0]["div"][0]["div"][0]["div"][0]["div"][1]["div"][1]["div"][5]["div"][8]["noscript"][0]:
        character_info["img"] = "https://www.prydwen.gg"+file['html'][0]["body"][0]["div"][0]["div"][0]["div"][0]["div"][1]["div"][1]["div"][5]["div"][8]["noscript"][0]["img"][0]["_attributes"]["srcset"].split(",")[2].split()[0]
    else:
        character_info["img"] = "https://www.prydwen.gg"+file['html'][0]["body"][0]["div"][0]["div"][0]["div"][0]["div"][1]["div"][1]["div"][5]["div"][8]["noscript"][0]["picture"][0]["img"][0]["_attributes"]["srcset"].split(",")[2].split()[0]    

def get_character_list(json) -> list[dict[str, str]]:
    character_list = []
    for character_div in json["html"][0]["body"][0]["div"][0]["div"][0]["div"][0]["div"][1]["div"][1]["div"][5]["span"]:
        character_info = {}
        character_info["name"] = character_div["div"][0]["span"][0]["a"][0]["div"][0]["span"][0]["_value"]
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
        output.append(f'{character["name"]}--Nikke--{character["img"]}')
    with open(output_file, 'w') as f:
        for item in output:
            f.write("%s\n" % item)

if __name__ == "__main__":
    main()
