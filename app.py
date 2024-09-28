from parsing import reading_format
import time
from multiprocessing import Manager, Pool, Process
from family import find_family
family={}
db={}


def output_from_queue(queue):
    while True:
        line = queue.get()
        if line is None:
            break

        find_family(line[0],family,line[1],db)


if __name__ == '__main__':
    start_time = time.time()


    manager = Manager()
    queue = manager.Queue()

    # Запускаем процесс для вывода из очереди
    output_process = Process(target=output_from_queue, args=(queue,))
    output_process.start()

    with Pool(processes=3) as pool:
        pool.starmap(reading_format, [(queue, 'main1.csv',0), (queue, 'main2.csv',1), (queue, 'main3.csv',2)])

    # Завершаем процесс вывода
    queue.put(None)  # Отправляем сигнал о завершении
    output_process.join()  # Ожидаем завершения процесса
    print("--- %s minutes ---" % ((time.time() - start_time)/60))
    print(db)


