from parsing import reading_format
import time
from multiprocessing import Manager, Pool, Process
from merge import final_compare

def check_que(que):
    a=0
    b=0
    c=0
    n=0
    while True:
        chis=que.get()
        match chis:
            case 0:
                a+=1
            case 1:
                b+=1
            case 2:
                c+=1
            case None:
                n+=1
        if (a>=1) and (b>=1) and (c>=1):
            a-=1
            b-=1
            c-=1
            final_compare("data/")
        if n==3:
            break


if __name__ == '__main__':
    start_time = time.time()
    m=Manager()
    que=m.Queue()


    output_process = Process(target=check_que, args=(que,))
    output_process.start()
    with Pool(processes=3) as pool:
        pool.starmap(reading_format, [('main1.csv',0,que),('main2.csv',1,que),('main3.csv',2,que)])

    output_process.join()  # Ожидаем завершения процесса





