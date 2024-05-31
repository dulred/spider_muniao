import pandas as pd

# 创建两个DataFrame，它们的索引是不同的
data1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]}, index=[0, 1])
data2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]}, index=[2, 3])

# 将两个DataFrame连接，保留原始索引
result_keep_index = pd.concat([data1, data2], ignore_index=False)
print("保留原始索引的结果:")
print(result_keep_index)

# 将两个DataFrame连接，生成新的整数索引
result_new_index = pd.concat([data1, data2], ignore_index=True)
print("\n生成新的整数索引的结果:")
print(result_new_index)
