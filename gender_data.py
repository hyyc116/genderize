#coding:utf8
from db_util import *
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from collections import Counter
from collections import defaultdict
import os

def gen_stats(filepath):

    ## generate gender with degree
    lines = []

    for line in open(filepath):
        line = line.strip()
        splits = line.split('====')
        

        ad_gender = splits[1]
        au_gender = splits[2]

        gender_type='MM'

        if ad_gender=='male':
            if au_gender=='male':
                gender_type='MM'
            elif au_gender=='female':
                gender_type='MF'
        elif ad_gender=='female':
            if au_gender=='male':
                gender_type='FM'
            elif au_gender=='female':
                gender_type='FF'

        degree = degree_process(splits[3])
        school = school_process(splits[4])
        year = year_process(splits[5])
        cats = cats_process(splits[6])
        country = splits[7]

        for cat in cats:
            lines.append([gender_type,degree,school,year,cat,country])

    degree_result =  generate_dict(lines,1)
    school_result = generate_dict(lines,2)
    year_result = generate_dict(lines,3)
    cat_result = generate_dict(lines,4)
    coutnry_result = generate_dict(lines,5)

    if os.path.exists('gender_data.js'):
        os.remove('gender_data.js')
        
    data = open('gender_data.js','a')

    data.write('var degree_data = {:};\n'.format(degree_result))
    data.write('var school_data = {:};\n'.format(school_result))
    data.write('var year_data = {:};\n'.format(year_result))
    data.write('var cat_data = {:};\n'.format(cat_result))
    data.write('var country_data = {:};\n'.format(coutnry_result))

    data.close()

def year_process(year):
    if year == '':
        return '-1111'
    return int(year)/10*10

def degree_process(degree):
    return degree

def school_process(school):
    return school

def country_process(country):
    return country

def cats_process(cat):
    cats = cat.split(";")
    fc =[]
    for cat in cats:
        # print cat
        if '-' in cat:
            for c in cat.split('-')[1].split(','):
                fc.append(c.replace('&#124','').replace('&#39',''))

    return list(set(fc))

def generate_dict(lines,index):
    attr_dict = defaultdict(list)
    # attr_count = defaultdict(int)
    for line in lines:
        gender_type = line[0]
        attr = line[index]
        if attr=='-1111':
            continue
        attr_dict[attr].append(gender_type)

        # attr_count[attr]+=1

    # print attr_dict
    ## 根据属性对应的数量进行排序
    count_index=0
    results = []
    for k,v in sorted(attr_dict.items(),key=lambda x:len(x[1]),reverse=True):

        result_dict = {}
        result_dict['State'] = k
        result_dict['freq'] = Counter(v)
        count_index+=1
        if count_index >9:
            break

        results.append(result_dict)


    return json.dumps(results)


if __name__ == '__main__':
    gen_stats(sys.argv[1])










