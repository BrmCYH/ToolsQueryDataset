
from  multiprocessing import Process,Pool
from typing import Dict, List
import os, time, random, requests, json
import itertools
import urllib3
from openai import OpenAI
from template import Combine_Template
from protocol import ChatMessage, Role
urllib3.disable_warnings()
class call:
    model = 'gpt-3.5-turbo'
    apikey=''
    url=""
    org = None
    target_dir = ''
    agent=OpenAI(base_url=url,api_key=apikey)
    @staticmethod
    def fun1(i,name,ith):
        print('Run task %s-%s (%s)...' % (name,ith, os.getpid()))
        start = time.time()
        time.sleep(random.random() * 3)

        message = Combine_Template.generate(i,name)
        response=call.get_answer(message)
#         print(response)
        call.store(f"{call.target_dir}/answer{name}_{ith}.json",i,response)
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
    def store(cls,files,q,a):
        try:
            with open(files,'w',encoding='utf-8')as f1:
                json.dump({"query":json.dumps(q),"answer":a},f1,ensure_ascii=False)
            print(f"write success {files}")
        except:
            print("{write failed.}")
            
    @classmethod
    def readi(cls,files):
        with open(files,'r',encoding='utf-8') as f1:
            return(json.load(f1))
        
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

    
if __name__=='__main__':

    pool = Pool(5) #创建一个5个进程的进程池
    call.model="gpt-3.5-turbo"
    call.apikey=''# apikey
    call.url="" # base_url
    call.org = None
    call.target_dir = ''# 数据集文件夹
    list1 = call.readi('')# func_calls 定义文件 List[Function_descriptions]
    if os.path.exists(call.target_dir):
        pass
    else:
        os.mkdir(f'{call.target_dir}')
    for i in range(1,2):# 排列组合的 C(len(list1),1) 
        for jth,combo in enumerate(itertools.combinations(list1, i),start=1): # 生成 tools组合
            pool.apply_async(func=call.fun1, args=(combo,i,jth))
    
    pool.close()
    pool.join()
    print('结束测试')