from flask import Flask
from flask import Blueprint
from flask import request
import requests
import json
import datetime
import logging
import time
from data2neo import data_to_neo

app = Flask(__name__)
app.logger.setLevel(logging.INFO) #log记录等级
handler = logging.FileHandler("info.log") #设置log文件
app.logger.addHandler(handler) #app的log文件加入info.log
current_time = datetime.datetime.now() #设置当前时间

beimin = Blueprint("beimin",__name__)


@beimin.route("re",methods=["POST"])               #入口
def re():
    try:
        i=1
        with open("data.txt", "r",encoding="utf-8") as file:
            for line in file:
                line = line.strip()  # 去除行尾的换行符和空格
                relation_extract(line)
                app.logger.info("第"+str(i)+"条数据处理完毕..")
                time.sleep(5)
                i = i+1
        data = {"suject": "Successful","status":111}
    except Exception as e:
        app.logger.info(e)
        data = {"suject": "无","status":111}
    
    return data
    
def relation_extract(text):
    try:
        prompt = '''
            你的任务是根据给定医学文本提取其中的关系。
            首先你需要提取文本中的“病症”，“关系”，“症状表现”。“人”不用提取。
            然后将“病症”和“症状表现”写入nodes, 在relationships中按照{"startNode": 病症, "endNode": 症状表现, "type": 关系}写入。
            文本:"风热感冒的症状是发烧"
            回答:{
                    "nodes": (
                        {"name": "风热感冒"},
                        {"name": "发烧"}
                    ),
                    "relationships": (
                        {"startNode": "风热感冒", "endNode": "发烧", "type": "症状"}
                    )
                }
            文本:"人当天睡不好的表现是人后一天头痛。"
            回答:{
                    "nodes": (
                        {"name": "睡不好"},
                        {"name": "后一天头痛"}
                    ),
                    "relationships": (
                        {"startNode": "睡不好", "endNode": "后一天头痛", "type": "表现"}
                    )
                }
            文本：
            ''' + text + "\n回答: "
        result = chat_fun(prompt)
        result = result.replace(" ","").replace("(","[").replace(")","]")
        app.logger.info(result)
        information = json.loads(result)
        data_to_neo(information) 
    except Exception as e:
        app.logger.info(e)
    



def extract_entity(response):    #提取实体
    start = response.find('{')
    end = response.find('}')
    if start != -1 and end != -1:
        response = response[start+1:end]
        return response
    else:
        return ""
    
def str_to_json(response):
    response = response.split('|')
   
    result = {"nodes":[],"relationships":[]}
    for r in response:
        temp = json.loads(r)
        if temp["type"] == "node":
            result["nodes"].append(temp)
        else:
            result["relationships"].append(temp)
    
    return result

def chat_fun(messages):

    gpt_api_url="http://172.16.3.175:9999/gptService/v1/sentenceZH" #这里填写合适的gpt url 

    headers = {
        "Content-Type": "application/json"
    }

    gpt_data = {}
    gpt_data['method'] = "gptChatReq"
    gpt_data['messages'] = [{'role': "user", 'content': messages}]  #配置get_data参数
    gpt_data['model'] = 'gpt-3.5-turbo'
    gpt_data['temperature'] = 0.6
    try:
        app.logger.info("Gennerating now")
        response = requests.post(gpt_api_url, headers=headers, data=json.dumps(gpt_data), timeout=50)  #访问gpt的api
        result_data = json.loads(response.text)
        result_data = result_data['data']               #处理数据
        choices = result_data['response']
        response = choices
    except Exception as e:
        app.logger.info(e)
        app.logger.info('调用gpt出错')

    return response