from parsing import reading_format
import time
from multiprocessing import Manager, Pool, Process
from family import find_family





if __name__ == '__main__':
    start_time = time.time()

    with Pool(processes=3) as pool:
        pool.starmap(reading_format, [('main1.csv',0),('main2.csv',1),('main3.csv',2)])


    print("--- %s seconds ---" % ((time.time() - start_time)))



