import os
import pandas as pd

# 获取当前脚本所在目录的父目录（即上级目录）
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)

# 找到父目录下的 spider 目录中的 data.csv 文件
csv_path = os.path.join(parent_directory, 'spider', 'data.csv')

# 输出文件夹
to_csv_path = os.path.join(parent_directory, 'spider','clean.csv')
print(csv_path)


# 读取数据文件
 
df.drop_duplicates(subset=['名字'])  #重复值处理

df["评分"] = df["评分"].astype(str)
df["评分"] = df["评分"].str.strip() #去除首尾空白

df['价格'] = df["价格"].replace("￥",'',regex=True)

df['可住'] = df['可住'].str.extract('(\d+)').astype(int) #提取数字并转换整数类型

df.to_csv(f'{to_csv_path}',index=False)
