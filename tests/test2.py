import time

# 记录开始时间
start_time = time.time()

# 执行一些操作
time.sleep(2)  # 让程序暂停 2 秒

# 记录结束时间
end_time = time.time()

# 计算运行时间
elapsed_time = end_time - start_time

print(f"程序运行时间: {elapsed_time} 秒")
