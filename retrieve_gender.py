#coding:utf-8

import urllib2
import sys
import json
import logging
reload(sys)
sys.setdefaultencoding('utf-8')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.DEBUG)


def retrieve_gender(name):
    url = 'https://api.genderize.io/?name={:}'.format(name)

    response = urllib2.urlopen(url)

    return response.read()

def retrieve_gender_list(namelist):
    length  = len(namelist)
    logging.info('length of name list : {:}'.format(len(namelist)))

    n = length/10+1

    for i in range(n):

        
        start = i*10
        end = (i+1)*10
        if end > length:
            end = length

        nameparams = ''
        for ni,name in enumerate(namelist[start:end]):
            nameparams+='name[{:}]={:}'.format(ni,name)
            nameparams+='&'
        url = 'https://api.genderize.io/?apikey=01071d7ac81d34877334b58423265a2c&'+nameparams[:-1]
        # print url
        response = urllib2.urlopen(url)

        parse_json(response.read())

        logging.info('progress of genderize : {:}/{:}'.format(i,n-1))

    logging.info('finish the progress of genderize')



def parse_json(result):
    objs = json.loads(result)
    for obj in objs:
        if obj['gender'] is None:
            sig = 'NO'
        else:
            sig = 'YES'
        print '{:}\t{:}\t{:}'.format(sig,obj['name'].decode('utf8',errors='ignore'),json.dumps(obj))


def parse_names_of_all(path):
    namelist = [name.strip() for name in open(path)]
    retrieve_gender_list(namelist)

if __name__ == '__main__':
    # result =  retrieve_gender('petersss')

    # namelist = ['peter','lily','lucy','lily','lucy','lily','lucy','lily','lucy','lily','lucy','lily','lucy','lily','lucy','lily','lucy','lily','lucy','lily','lucy','lily','lucy']
    # retrieve_gender_list(namelist)

    parse_names_of_all(sys.argv[1])



