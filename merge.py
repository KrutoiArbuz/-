import pandas as pd
from pathlib import Path
import os
import json


def merge_json_files(directory_path):

    final_family = {}
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            with open(os.path.join(directory_path, filename), 'r',encoding="utf-8") as file:
                data = json.load(file)
                print(len(data))
                final_family.update(data)
    return final_family
#
#
# def final_compare(final_family):
#     keys=list(final_family.keys())
#     for i in range(len(keys)):
#         for j in range(i+1,len(keys)+1):

final_family=(merge_json_files("data/"))
print(len(final_family))