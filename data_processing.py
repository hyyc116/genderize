#coding:utf8
from db_util import *

def retrive_all_unique_names():
    query_op = dbop()
    sql = 'select first_name,middle_name,last_name from  proquest_article_authorname'
    cursor  = query_op.query_database(sql)

    name_set = []
    for row in cursor:
        name  = ','.join(row)
        name_set.append(name)

    print len(name_set)

    name_list =list(set(name_set))

    print len(name_list)

    open('unique_names.txt','w').write('\n'.join(name_list))

if __name__ == '__main__':
     retrive_all_unique_names() 
