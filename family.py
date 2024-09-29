import json
import uuid
import random
import string
from comparison import compar



def generate_unique_key(length=8):
    characters = string.ascii_letters + string.digits
    # Генерируем случайную строку заданной длины
    key = ''.join(random.choice(characters) for _ in range(length))
    return key

# функция поиска семьи
def find_family(string,family,num_db):

    # проходимся по ключам кортежа
    for i in list(family.keys()):
        if compar(string,family[i]["string"],num_db)==True:
            # если строка больше мастер строки по кол-ву значений
            if (len(string)>len(family[i]["string"])):
                family[i]["string"]=string
            # добавляем айди строки в семью
            family[i]['ids'].append(string['uid'])



    i=generate_unique_key()
    # создание семьи
    family[i]={"string":string,"num_db":num_db,"ids":[string['uid']]}


    return 0

