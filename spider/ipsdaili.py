import requests
import time
import re
import json
import os
import sys

# 加入可识别的路径 PYTHONPATH
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)

sys.path.append(parent_directory)


from utils.directory_utils import DirectoryUtils as Du
# 爬取的文件夹
dir_utils = Du()
output_path = dir_utils.get_path('data', 'ipdaili.txt')


class daili:

    # 1.发送请求，获取响应
    def send_request(self,page):
        print(f"=============正在抓取第{page}页===========")
        # 目标网页，添加headers参数 
        base_url = f'https://www.kuaidaili.com/free/inha/{page}/'
        headers = {'user-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60"}
        time.sleep(4)
        # 发送请求：模拟浏览器发送请求，获取响应数据
        response = requests.get(base_url,headers=headers)   
        data = response.text

        return data

    # 2.解析数据
    def parse_data(self,data):
        
        # 使用正则表达式匹配 JavaScript 代码中的 fpsList
        pattern = re.compile(r'const\s+fpsList\s+=\s+(.*?);', re.DOTALL)
        match = pattern.search(data)
        
        if match:
            # 提取 JSON 数据
            json_data = match.group(1)
            # 解析 JSON 数据
            parse_list = json.loads(json_data)
            # 输出数据
            for item in parse_list:
                print(f"IP: {item['ip']}, Port: {item['port']}")
        else:
            print("fpsList not found in HTML data")
        return parse_list

    # 4.检测代理IP
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

    # 5.保存到文件
    def save(self,can_use):
        
        with open(f'{output_path}', 'w') as file:    
            for i in range(len(can_use)):
                s = str(can_use[i])+ '\n'
                file.write(s)

    # 实现主要逻辑
    def run(self):
        proxies_list = []
        # 实现翻页，我这里只爬取了四页（可以修改5所在的数字）
        for page in range(1,5):
            data = self.send_request(page)
            parse_list = self.parse_data(data)
            # 3.获取数据
            for item in parse_list:
                proxies_dict  = {}
                ip_num = item['ip']
                port_num = item['port']
                http_type = "http"
                proxies_dict[http_type] = f"http://{ip_num}:{port_num}"

                proxies_list.append(proxies_dict)
            print(proxies_dict)
        
        print("获取到的代理IP数量：",len(proxies_list))

        can_use = self.check_ip(proxies_list)

        print("能用的代理IP数量：",len(can_use)) 
        print("能用的代理IP:",can_use) 

        self.save(can_use)

if __name__ == "__main__": 
    dl = daili()
    dl.run()
