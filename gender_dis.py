#coding:utf8
from db_util import *
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from collections import Counter

def get_gender_data(genderpath):

    name_dict={}
    for line in open(genderpath):
        line = line.strip()
        splits = line.split('\t')
        if splits[0]=='YES':
            # g = json.loads(splits[-1])['gender']
            name_dict[splits[1]] = splits[-1]

    adviser_genders=[]
    author_genders=[]
    sql='select proquest_article_adviser.ditm_id,ADVISER_NAME,FIRST_NAME from proquest_article_adviser,proquest_article_authorname where proquest_article_adviser.ditm_id = proquest_article_authorname.ditm_id'

    query_op = dbop()
    query_op.connect_aws()
    cursor  = query_op.query_database(sql)

    paper_count =0 
    for row in cursor:
        adviser_first_name = row[1].split()[0].lower()
        author_first_name = row[2].lower()

        paper_count+=1

        adviser_gender = gender_of_name(adviser_first_name)
        author_gender = gender_of_name(author_first_name)

        if adviser_gender is not None and author_gender is not None:
            adviser_genders.append(adviser_gender)
            author_genders.append(author_gender)

    print paper_count,len(adviser_genders)
        


def gender_of_name(name,name_dict):
    if '-' in name:
        splits = name.split('-')
        g = ('-1',0)
        for s in splits:
            if name_dict.get(s,-1)!=-1:

                obj = json.loads(name_dict[s])
                ge = obj['gender']
                gp = obj['probability']
                if gp>g[1]:
                    g = (ge,gp)

        if g[0]!='-1':
            return g[0]
        else:
            return None
    else:
        return json.loads(name_dict[name])['gender']

if __name__ == '__main__':
    get_gender_data(sys.argv[1])





