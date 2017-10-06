#coding:utf8
from db_util import *
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from collections import Counter
from collections import defaultdict

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

        degree = splits[3]
        school = splits[4]
        year = splits[5]
        cats = splits[6]
        country = splits[7]

        lines.append([gender_type,degree,school,year,cats,country])

    print generate_dict(lines,1)



def generate_dict(lines,index):
    attr_dict = defaultdict(list)
    # attr_count = defaultdict(int)
    for line in lines:
        gender_type = line[0]
        attr = line[index]

        attr_dict[attr].append(gender_type)

        # attr_count[attr]+=1

    # print attr_dict
    result_dict = {}
    ## 根据属性对应的数量进行排序
    count_index=0
    for k,v in sorted(attr_dict.items(),key=lambda x:len(x[1]),reverse=True):
        print k,len(v)
        result_dict['State'] = k
        result_dict['freq'] = Counter(v)
        count_index+=1
        if count_index >9:
            break


    return result_dict


if __name__ == '__main__':
    gen_stats(sys.argv[1])










