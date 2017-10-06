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


    # sql='''
    #     select proquest_article_adviser.ditm_id,ADVISER_NAME,FIRST_NAME,DEGREE,SCHOOL_NAME,DEGREE_YEAR,SUBJECTS,COUNTRY 
    #     from proquest_article_adviser,proquest_article_authorname, proquest_raw
    #     where proquest_article_adviser.ditm_id = proquest_article_authorname.ditm_id
    #     and proquest_raw.ditm_id = proquest_article_authorname.ditm_id
    #     '''

    sql='''
        select ditm_id,DITM_ADVISER,AUTHOR_NAME,DEGREE,SCHOOL_NAME,DEGREE_YEAR,SUBJECTS,COUNTRY 
        from proquest_raw
        '''

    query_op = dbop()
    query_op.connect_aws()
    cursor  = query_op.query_database(sql)
    lines = []
    paper_count =0 
    for row in cursor:
        ditm_id = row[0]
        print row[0],row[1]
        adviser_first_name = row[1].split()[0].lower()
        author_first_name = row[2].split(',')[1].lower()
        degree = row[3]
        school_name = row[4]
        degree_year = row[5]
        subject = row[6]
        country = row[7]

        paper_count+=1

        adviser_gender = gender_of_name(adviser_first_name,name_dict)
        author_gender = gender_of_name(author_first_name,name_dict)

        if adviser_gender is not None and author_gender is not None:
            lines.append('===='.join([str(a) for a in [ditm_id,adviser_gender,author_gender,degree,school_name,degree_year,subject,country]]))

    print paper_count,len(lines),len(lines)/float(paper_count)

    open('proquest_genders.txt','w').write('\n'.join(lines))


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

        if name_dict.get(name,-1)!=-1:

            return json.loads(name_dict[name])['gender']
            
        else:
            return None

if __name__ == '__main__':
    get_gender_data(sys.argv[1])






