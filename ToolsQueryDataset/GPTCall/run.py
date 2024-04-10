
from  multiprocessing import Process, Pool
import multiprocessing as mp

from typing import Dict, List, Optional, overload
import os, time, random, requests, json

import urllib3
import argparse

from template import Combine_Template
from protocol import ChatMessage, Role
import itertools

urllib3.disable_warnings()
class call:
    model = 'gpt-3.5-turbo'
    apikey=''
    url=""
    org = None
    target = ''
    @staticmethod
    def fun1(i,name,ith):
        print('Run task %s-%s (%s)...' % (name,ith, os.getpid()))
        start = time.time()
        time.sleep(random.random() * 3)

        message = Combine_Template.generate(i,name)
        response=call.get_answer(message)
        call.store(os.path.join(call.target_dir,f"answer{name}_{ith}.json"),i,response)
        end = time.time()
        print('Task %s Message: %s,runs %0.2f seconds.' % (name, response, (end - start)))
    @classmethod
    def request_chatgpt(cls, parameters):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {cls.apikey}",
        }


        with requests.post(cls.url, headers=headers, json=parameters, verify=False,
                     timeout=10000, stream=False) as response:

            res=response.json()

            return res['choices'][0]['message']['content']
    @classmethod
    def readi(cls,files:List[str]):
        xlist=[]
        for file in files:
            try:
                with open(file,'r',encoding='utf-8') as f1:
                    xlist.extend(json.load(f1))
            except FileNotFoundError:
                print(f"{file} not found")
            except json.JSONDecodeError:
                print(f"{file} can not format to json")

        return xlist
    @classmethod
    def store(cls,files,q,a):
        try:
            with open(files,'w',encoding='utf-8')as f1:
                json.dump({"query":json.dumps(q),"answer":a},f1,ensure_ascii=False)
            print(f"write success {files}")
        except:
            print("{write failed.}")
            

    @classmethod
    def get_answer(cls, message:List[ChatMessage]):

        parameters = {
            "model": cls.model,
            "messages": message,
            "stream": False,
            "temperature":0.8
        }

        response = cls.request_chatgpt(parameters)
        return response
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target_dir', type = str, default='glaive', help='target_dir')
    parser.add_argument('--apikey', type = str, default='', help='apikey')
    parser.add_argument('--url', type = str, default='', help='url')
    parser.add_argument('--org', type = Optional[str], default=None, help='org')
    parser.add_argument('--model', type = str, default='gpt-3.5-turbo', help='model')
    parser.add_argument('--func_defin_file', type = str, default='', help='func_defin_file')
    parser.add_argument('--pool_size', type = int, default=mp.cpu_count(), help='Processes pool_size')
    parser.add_argument('--combination_Max_size', type = int, default=4, help='One problem contains max 4 tools')
    args = parser.parse_args()
    call.target_dir = args.target_dir
    call.model=args.model
    call.apikey=args.apikey
    call.url=args.url # base_url
    call.org = args.org 

    pool = Pool(args.pool_size) #创建一个5个进程的进程池

    
    if os.path.isfile(args.func_defin_file):
        print('file')
        func_files=[args.func_defin_file]
    else:
        for dirname, _, filenames in os.walk(args.func_defin_file):
            func_files=[os.path.join(dirname,filename) for filename in filenames] 
    try:
        list1 = call.readi(func_files) # func_calls 定义文件 List[Function_descriptions]
    except :
        raise f"floder {args.func_defin_file} not found"
    
    if os.path.exists(call.target_dir):
        pass
    else:
        os.makedirs(f'{call.target_dir}')
    print(f"tools number:{len(list1)},{func_files}")

    for i in range(1,args.combination_Max_size+1): # 排列组合的 C(len(list1),1) 
        for jth,combo in enumerate(itertools.combinations(list1, i),start=1): # 生成 tools组合
            pool.apply_async(func=call.fun1, args=(combo,i,jth))
    
    pool.close()
    pool.join()
    print('结束')
    
if __name__=='__main__':
    main()
    