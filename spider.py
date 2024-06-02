import requests
import random
from lxml import etree
import pandas as pd
import time

def getip():
    with open('ipdaili.txt') as f
        iplist = f.readlines()
        proxy = iplist[random.randint(0, len(iplist) - 1)]
        proxy = proxy.replace('\n', "")
        proxies = {
            'http': 'http://' + str(proxy)
        }
    return proxies

cookie = 'Bsksdjd=down_app; SECKEY_ABVK=jCZbPBoCKuFYu78EPu1FAlxXDay2LutyLp/AXPuqp0g%3D; BMAP_SECKEY=Z0yeN76NJShVf9Jv6CISBmO_BAD0ignCp7PjuNjU6yjOEBAE9utmBqfAJ4W2FmKwmuXYcPq9Z1QLX_2v5eyxb2Dt21eWKHJau342DuQZXP-zhmRAfcY8h2mJaepfc6tavJLYf12HRMCRXMHnOpO6myOpmOOz70red-bRzxJxaro_Z_4EwRiwcqPiorGK-mkLfHI1oR7HX0U0enS7EcsRew; route=e028bf8e2ee7f213721872762d23fbc1; sl-session=lhnyctWZXGa1FoVwR7U+Rw==; ASP.NET_SessionId=lgeuc0ovid54jtifnit1zigr; Front_LoginUserKey=85EFE19FA89BC48015694D9C083B64D99B88ABF09745E1AE9EDF5CA53D923A0186FB6FCEFFF1EFC693EF6BFA09CAC0117EA7F778088738D1485F009325A70C5E3E1BB8869B37C507CBDF16DB30406E044757981ADAA83FD60886BC60B23643186E981CE1A856F84347E47B8751D007F7E2C783B85124308FBAE43A08FE0E6F46F1E74314DBA5B892AFFEEB0131D7CD4B7374FE15DC71DAC7C5D6070CF45DC34AEE4D335D56B8BA16638EA015E9C959692A67D00ADAC994FF5537D0AB0E9F0760FF7E002FE1A90BFF'
def spider(city, page):
    url = f'https://www.muniao.com/{city}/null-0-0-0-0-0-0-0-{page}.html?tn=mn19091015'
    headers = [
        {
            'user-Agent': "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
            'cookie': cookie
        },
        {
            'user-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
            'cookie': cookie
        },
        {
            'user-Agent': "Mozilla/5.0 (compatibel; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
            'cookie': cookie
        },
        {
            'user-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
            'cookie': cookie
        },
        {
            'user-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
            'cookie': cookie
        },
        {
            'user-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
            'cookie': cookie
        },
        {
            'user-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
            'cookie': cookie
        },
    ]
    resp = requests.get(url,headers=random.choice(headers), proxies=getip())

    html = resp.text

    # 使用lxml解析html
    tree = etree.HTML(html)
    title = tree.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/div/div[1]/div[1]/div[1]/a/text()')
    score = tree.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/div/div[2]/div[2]/div[2]/span/text()')
    hx = tree.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/div/div[1]/div[1]/div[2]/p/span[1]/text()')
    cz_type = tree.xpath(' /html/body/div[5]/div[1]/div[1]/ul/li/div/div[1]/div[1]/div[2]/p/span[2]/text()')
    kz = tree.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/div/div[1]/div[1]/div[2]/p/span[3]/text()')
    price = tree.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/div/div[1]/div[1]/div[2]/div[2]/span/text()')
    img_url = tree.xpath('/html/body/div[5]/div[1]/div[1]/ul/li/div/div[2]/div[1]/a/img/@src')


    # 将数据存储到DataFrame里面
    data = pd.DataFrame({
        '名字':title,
        '评分':score,
        '户型':hx,
        '出租类型':cz_type,
        '可住':kz,
        '价格':price,
        '图片地址':img_url,
        '城市':city
    })
    
    return data

all_data = pd.DataFrame()#创建一个空的DataFrame
citys = ['chengdu', 'shanghai']
for city in citys:
    for page in range(1,11):
        time.sleep(4)
        print(f'{city}第{page}页爬取中..')
        data = spider(city, page)
        all_data = pd.concat([all_data, data], ignore_index=True)

all_data.to_csv('data.csv', index=False)