from func import *
import time

if __name__ == '__main__':
    # delete_search('data_analyst&&france')

    t0 = time.time()
    delete_search('data_analyst&&italy')
    create_new_search('data_analyst', 'italy')

    t1 = time.time() - t0
    print(f'Time elapsed: {t1}s')
    # update_searches()
    # db = SqlConnexion('jobs.db')
    # sql = 'SELECT link FROM results'
    # db.curr.execute(sql)
    # links = db.curr.fetchall()
    # [print(link) for link in links]





