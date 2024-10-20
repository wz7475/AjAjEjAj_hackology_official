import os
import json


merged_jsons = []

for single_json in os.listdir():
    if single_json == "shop_data_merged.json":
        continue
    
    if single_json.endswith(".json"):
        with open(single_json, 'r', encoding="utf-8") as fh:
            try:
                json_file = json.load(fh)
            except json.decoder.JSONDecodeError:
                print(f"{single_json} is empty")
                continue
        
        new_json = json_file["data"]
        lat, lon = single_json.replace(".json", "").split("_")
        new_json.update({
            "lat": lat,
            "lon": lon
        })
        merged_jsons.append(new_json)

with open("shop_data_merged.json", 'w', encoding="utf-8") as fh:
    json.dump(merged_jsons, fh, ensure_ascii=False, indent=4)
