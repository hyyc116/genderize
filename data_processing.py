#coding:utf8
from db_util import *
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from collections import Counter

def retrive_proquest_unique_names():
    query_op = dbop()
    query_op.connect_aws()
    sql = 'select first_name,middle_name,last_name from  proquest_article_authorname'
    cursor  = query_op.query_database(sql)

    name_set = []
    for row in cursor:
        # name  = ','.join(row)
        name_set.append(row[0].lower())

    print 'article authors:',len(name_set)

    name_list =list(set(name_set))

    print 'unique article authors:',len(name_list)

    ## add advisors' name
    sql = 'select adviser_name from proquest_article_adviser'

    '''这里有很多长度大于四的如何处理？'''

    cursor = query_op.query_database(sql)
    for row in cursor:
        names = row[0].split()
        name_list.append(names[0].lower())

    print 'add  advisors:',len(name_list)


    name_list = list(set(name_list))

    print 'unique add advisors]',len(name_list)


    open('unique_names.txt','w').write('\n'.join(name_list))
    return name_list


def retirve_aminer_unique_names(aminer_names,other_names):
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
        name_List.append(name.encode('utf-8', 'ignore').lower())

    print len(name_List)
    name_set = list(set(name_List))
    print len(name_set)


    open('aminer_names.txt','w').write('\n'.join(name_set))
    open('multi.txt','w').write('\n'.join(multis))

    other_names.extend(name_set)

    print len(other_names)


    ## 对名字进行处理
    ss = ['`','#',"&","\\","'",'.','?','<','>','_']
    all_names=[]
    for name in other_names:
        is_c = True

        if name.strip()=='':
            continue
            
        for s in ss:
            if s in name:
                is_c = False
                break
        
        if is_c:
            if '-' in name:
                ns = [a.strip() for a in name.split('-') if len(a.strip())>1]
                all_names.extend(ns)
            else:

                all_names.append(name.strip().replace(',',''))

    all_names = list(set(all_names))

    print 'length of final names:',len(all_names)

    open('all_names.txt','w').write('\n'.join(all_names))

def percent_of_request(genderpath):
    name_dict={}
    for line in open(genderpath):
        line = line.strip()
        splits = line.split('\t')
        if splits[0]=='YES':
            g = json.loads(splits[-1])['gender']
            name_dict[splits[1]] = g


    query_op = dbop()
    query_op.connect_aws()
    sql = 'select first_name,middle_name,last_name from  proquest_article_authorname'
    cursor  = query_op.query_database(sql)

    name_list = []
    for row in cursor:
        # name  = ','.join(row)
        name_set.append(row[0].lower())

    print 'article authors:',len(name_set)

    ## add advisors' name
    sql = 'select adviser_name from proquest_article_adviser'

    '''这里有很多长度大于四的如何处理？'''

    cursor = query_op.query_database(sql)
    for row in cursor:
        names = row[0].split()
        name_list.append(names[0].lower())

    print 'add  advisors:',len(name_list)

    genders = []
    for name in name_list:
        if name_dict.get(name,-1)!=-1:
            genders.append(name_dict[name])
        else:
            if '-' in name:
                splits = name.split('-')
                g = ('-1',0)
                for s in splits:
                    if name_dict.get(s,-1)!=-1 and name_dict[s]>g[1]:
                        g = (s,name_dict[s])

                if g[0]!='-1':
                    genders.append(g[0])

    gc = Counter(genders)
    print 'total:',len(name_list),'with gender:',len(genders),'percent = {:.2f}'.format(len(genders)/float(len(name_list)))
    for g in gc.keys():
        print 'gender:',g,'num:',gc[g]

if __name__ == '__main__':
    # anames = retrive_proquest_unique_names()
    # retirve_aminer_unique_names(sys.argv[1],anames)
    percent_of_request(sys.argv[1])
    
