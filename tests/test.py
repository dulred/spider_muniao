import requests
import time
from lxml import etree
import re
import json

def send_request(page):
    print(f"=============正在抓取第{page}页===========")
    # 目标网页，添加headers参数 
    base_url = f'https://www.kuaidaili.com/free/inha/{page}/'
    headers = {'user-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60"}

    # 发送请求：模拟浏览器发送请求，获取响应数据
    response = requests.get(base_url,headers=headers)   
    data = response.text

    return data

def parse_data(data):
        
    # 数据转换
    html_data =  etree.HTML(data)
    # 分组数据
    parse_list = html_data.xpath('/html/body/div[3]/main/div/section/div/div[2]/div/div/div[2]/div/table/tbody/tr/td[1]')

    return parse_list

def check_ip(self,proxies_list):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

    can_use = []
    for proxies in proxies_list:
        try:
            response = requests.get('https://www.baidu.com/',headers=headers,proxies=proxies,timeout=0.1)
            if response.status_code == 200:
                can_use.append(proxies)

        except Exception as e:
            print(e)
            
    return can_use

if __name__ == "__main__":
    data = send_request(1)
    # xx = parse_data(data = data)

    
    
    # print(data)
