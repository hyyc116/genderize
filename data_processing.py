#coding:utf8
from db_util import *
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def retrive_proquest_unique_names():
    query_op = dbop()
    query_op.connect_aws()
    sql = 'select first_name,middle_name,last_name from  proquest_article_authorname'
    cursor  = query_op.query_database(sql)

    name_set = []
    for row in cursor:
        # name  = ','.join(row)
        name_set.append(row[0])

    print 'article authors:',len(name_set)

    name_list =list(set(name_set))

    print 'unique article authors:',len(name_list)

    ## add advisors' name
    sql = 'select adviser_name from proquest_article_adviser'

    '''这里有很多长度大于四的如何处理？'''

    cursor = query_op.query_database(sql)
    for row in cursor:
        names = row[0].split()
        name_list.append(names[0])

    print 'add  advisors:',len(name_list)


    name_list = list(set(name_list))

    print 'unique add advisors]',len(name_list)


    open('unique_names.txt','w').write('\n'.join(name_list))


def retirve_aminer_unique_names(aminer_names):
    author_list = json.loads(open(aminer_names).read())['RECORDS']
    name_List =[]
    length =  len(author_list)
    process =0
    multi_count=0
    multis = []
    for author in author_list:
        
        process+=1

        if process%10000 ==1:
            print 'progress',process,'/',length

        splits = author['lastname_firstname'].split(',')

        if len(splits)!=2:
            multis.append(author['lastname_firstname'].encode('utf-8', 'ignore'))
            multi_count+=1
            continue

        last,first = splits


        name = first
        name_List.append(name.encode('utf-8', 'ignore'))

    print len(name_List)
    name_set = list(set(name_List))
    print len(name_set)


    open('aminer_names.txt','w').write('\n'.join(name_set))
    open('multi.txt','w').write('\n'.join(multis))


if __name__ == '__main__':
    retrive_proquest_unique_names()
    retirve_aminer_unique_names(sys.argv[1])
    
