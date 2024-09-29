from comparison import compar
import os
import json
import csv




def final_compare(directory_path):

    final_family = {}
    for filename in os.listdir(directory_path):
            if filename.endswith('.json'):
                with open(os.path.join(directory_path, filename), 'r',encoding="utf-8") as file:
                    data = json.load(file)


                    final_family.update(data)

    keys=list(final_family.keys())
    with open("table_results.csv", mode='w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(['id_is1', "id_is2", "id_is3"])
        for i in range(len(keys)):
            num_dbi = final_family[keys[i]]["num_db"]
            ids=[[],[],[]]
            match num_dbi:
                case 0:
                    ids[0] = final_family[keys[i]]['ids']
                case 1:
                    ids[1] = final_family[keys[i]]['ids']
                case 2:
                    ids[2] = final_family[keys[i]]['ids']
            for j in range(i+1,len(keys)):
                num_dbj=final_family[keys[j]]["num_db"]
                if num_dbi==2 or num_dbj==2:
                    if compar(final_family[keys[i]]['string'],final_family[keys[j]]['string'],2):
                        ids[num_dbj]+=final_family[keys[j]]['ids']
                elif num_dbi==0 or num_dbj==0:
                    if compar(final_family[keys[i]]['string'],final_family[keys[j]]['string'],0):
                        ids[num_dbj]+=final_family[keys[j]]['ids']
                else:
                    if compar(final_family[keys[i]]['string'],final_family[keys[j]]['string'],1):
                        ids[num_dbj]+=final_family[keys[j]]['ids']

            result_ids=[]
            for t in range(3):
                result_ids.append(list(set(ids[t])))
            writer.writerow([result_ids[0],result_ids[1],result_ids[2]])
            file.flush()


