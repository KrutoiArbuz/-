import json
import uuid
import random
from comparison import compar

def fck(string1,string2):
    return string1>=string2

def find_family(string,family,num_db,final_db):

    for i in list(family.keys()):
        if compar(string,family[i]["string"],num_db)==True:
            family[i]["string"]=string

            family[i]['ids'].append(string['uid'])

            if ( family[i]["id"] in final_db.keys()):

                final_db[family[i]["id"]][num_db].append(string['uid'])
            else:
                match num_db:
                    case 0:
                        final_db[family[i]["id"]] = [[string['uid']], [], []]
                    case 1:
                        final_db[family[i]["id"]] = [[], [string['uid']], []]
                    case 2:
                        final_db[family[i]["id"]] = [[], [], [string['uid']]]
            return 0

    k=-1
    while True:
        k = random.randint(0,100000)
        if not str(k) in family.keys():
            break

    i=str(k)
    family[i]={"string":string,"id":str(uuid.uuid4()),"ids":[string['uid']]}



    if ( family[i]["id"] in final_db.keys()):
        final_db[family[i]["id"]][num_db]=string['uid']
    else:
        match num_db:
            case 0:
                final_db[family[i]["id"]]=[[string['uid']],[],[]]
            case 1:
                final_db[family[i]["id"]]=[[],[string['uid']],[]]
            case 2:
                final_db[family[i]["id"]]=[[],[],[string['uid']]]
    return 0

