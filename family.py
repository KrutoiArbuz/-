import json
import uuid
import random
from comparison import compar


# функция поиска семьи
def find_family(string,family,num_db,final_db):
    # проходимся по ключам кортежа
    for i in list(family.keys()):
        if compar(string,family[i]["string"],num_db)==True:
            # если строка больше мастер строки по кол-ву значений
            if (len(string)>len(family[i]["string"])):
                family[i]["string"]=string
            # добавляем айди строки в семью
            family[i]['ids'].append(string['uid'])
            # если есть НАШЕ айди в итоговой бд, заполняем его
            if ( family[i]["id"] in final_db.keys()):
                final_db[family[i]["id"]][num_db].append(string['uid'])
            else:
                # если нет, то в зависимости от бд откуда пришла строка
                match num_db:
                    case 0:
                        final_db[family[i]["id"]] = [[string['uid']], [], []]
                    case 1:
                        final_db[family[i]["id"]] = [[], [string['uid']], []]
                    case 2:
                        final_db[family[i]["id"]] = [[], [], [string['uid']]]
            return 0
    # создание какой то переменной
    k=-1
    while True:
        k = random.randint(0,100000)
        if not str(k) in family.keys():
            break

    i=str(k)
    # создание семьи
    family[i]={"string":string,"id":str(uuid.uuid4()),"ids":[string['uid']]}

    # если есть НАШЕ айди в итоговой бд, заполняем его
    if ( family[i]["id"] in final_db.keys()):
        final_db[family[i]["id"]][num_db]=string['uid']
    else:
        # если нет, то в зависимости от бд откуда пришла строка
        match num_db:
            case 0:
                final_db[family[i]["id"]]=[[string['uid']],[],[]]
            case 1:
                final_db[family[i]["id"]]=[[],[string['uid']],[]]
            case 2:
                final_db[family[i]["id"]]=[[],[],[string['uid']]]
    return 0

