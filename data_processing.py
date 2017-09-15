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

    print 'article authors:',len(name_set)

    name_list =list(set(name_set))

    print 'unique article authors:',len(name_list)

    ## add advisors' name
    sql = 'select adviser_name form proquest_article_adviser'

    cursor = query_op.query_database(sql)
    for row in cursor:
        names = row[0].split()
        if len(names)==3:
            name_list.append(','.join(names))
        elif len(names)==2:
            name_list.append(','.join([names[0],'',names[1]]))
        elif len(names)>3:
            print row[0]
        elif len(names)==1:
            print row[0]

    print 'add  advisors:',len(name_list)

    name_list = list(set(name_list))

    print 'unique add advisors',len(name_list)


    open('unique_names.txt','w').write('\n'.join(name_list))

if __name__ == '__main__':
     retrive_all_unique_names() 
