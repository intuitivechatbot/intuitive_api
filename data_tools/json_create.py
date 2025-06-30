import os
import json
from glob import glob
input_folder = "summaries"
output_json = "combined_summaries.json"

all_summaries = {}

for txt_file in glob(os.path.join(input_folder, "*.txt")):
    with open(txt_file, "r", encoding="utf-8") as f:
        content = f.read()
    file_name = os.path.basename(txt_file)
    all_summaries[file_name] = content

with open(output_json, "w", encoding="utf-8") as f:
    json.dump(all_summaries, f, indent=4, ensure_ascii=False)

print(f"Combined summaries have been saved to {output_json}.")