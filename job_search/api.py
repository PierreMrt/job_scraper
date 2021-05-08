from db_management import SqlConnexion
from func import DB_NAME


def search_keywords(search_key, keywords):
    db = SqlConnexion(DB_NAME)

    sql = "SELECT * FROM results WHERE search_key='{0}' ".format(search_key)
    for kw in keywords:
        sql += "AND description LIKE '%{0}%' ".format(kw)

    db.curr.execute(sql)
    results = db.curr.fetchall()
    
    return results

if __name__ == '__main__':
    search_key = 'data_analyst&&france'
    kw = ['python', 'sql']
    results = search_keywords(search_key, kw)
    print(results)