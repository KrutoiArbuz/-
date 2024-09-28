import csv
from xaxaton import *

def reading_format(queue,url,num_db):
    k=1
    with open(url,encoding='utf-8') as db:
        db_reader = csv.reader(db,delimiter=',')


        for string in db_reader:
            if k == 1:
                k=0
                continue

            match num_db:
                case 0:
                    uid=string[0]
                    full_name=normal_fio(string[1])
                    email=normal_email(string[2])
                    address=normal_address(string[3])
                    sex=string[4]
                    birthdate=normal_date(string[5])
                    phone=normal_mobile_phone(string[6])
                    return_string ={"uid":uid,"full_name":full_name,"email":email,"address":address,"sex":sex,"birthdate":birthdate,"phone":phone}
                case 1:
                    uid = string[0]

                    name = normal_fio(string[1]+string[2]+ string[3])
                    birthdate= normal_date(string[4])
                    phone= normal_mobile_phone(string[5])
                    address= normal_address(string[6])
                    return_string ={"uid":uid,"full_name":name,"birthdate":birthdate,"phone":phone,"address":address,email:""}
                case 2:
                    uid = string[0]
                    name = normal_fio(string[1])
                    email= normal_email(string[2])
                    birthdate= normal_date(string[5])
                    sex= string[6]
                    return_string ={"uid":uid,"full_name":name,"email":email,"birthdate":birthdate,"sex":sex}





            queue.put([return_string,num_db])



