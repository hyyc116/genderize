#coding:utf8
from db_util import *
import json

def retrive_proquest_unique_names():
    query_op = dbop()
    query_op.connect_aws()
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
    sql = 'select adviser_name from proquest_article_adviser'

    '''这里有很多长度大于四的如何处理？'''

    cursor = query_op.query_database(sql)
    for row in cursor:
        names = row[0].split()
        if len(names)==3:
            name_list.append(','.join(names))
        elif len(names)==2:
            name_list.append(','.join([names[0],'',names[1]]))
        elif len(names)>3:
            if ',' in row[0]:
                names = row[0].split(',')[0].split()
                name_list.append(','.join([ names[0],' '.join(names[1:-1]),names[-1]]))

        elif len(names)==1:
            name_list.append(','.join([names[0],'','']))

    print 'add  advisors:',len(name_list)


    name_list = list(set(name_list))

    print 'unique add advisors]',len(name_list)


    open('unique_names.txt','w').write('\n'.join(name_list))


def retirve_aminer_unique_names(aminer_names):
    author_list = json.loads(open(aminer_names).read())['RECORDS']
    name_List =[]
    length =  len(author_list)
    process =0
    for author in author_list:
        
        process+=1

        if process%10000 ==1:
            print 'progress',process,'/',length

        splits = author['lastname_firstname'].split(',')

        if len(splits)!=2:
            print splits
            continue

        first,last = author['lastname_firstname']

        mid =  author['middlename']
        if mid is None or mid=='null':
            mid = ""

        name = ','.join([first,mid,last])
        name_List.append(name)

    print len(name_List)
    name_set = list(set(name_List))
    print len(name_set)


    open('aminer_names.txt','w').write('\n'.join(name_set))


if __name__ == '__main__':
    retirve_aminer_unique_names(sys.argv[1])
    
