import os
import pandas as pd
import sys

# 加入可识别的路径 PYTHONPATH
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)

sys.path.append(parent_directory)


from utils.directory_utils import DirectoryUtils as Du
# 爬取的文件夹
dir_utils = Du()

open_path = dir_utils.get_path('data', 'data.csv')
output_path = dir_utils.get_path('data', 'clean.csv')


# 读取数据文件
df = pd.read_csv(open_path)

df.drop_duplicates(subset=['名字'])  #重复值处理

df["评分"] = df["评分"].astype(str)
df["评分"] = df["评分"].str.strip() #去除首尾空白

df['价格'] = df["价格"].replace("￥",'',regex=True)

df['可住'] = df['可住'].str.extract('(\d+)').astype(int) #提取数字并转换整数类型


df.to_csv(f'{output_path}',index=False)
