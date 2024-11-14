import pandas as pd
from pulp import LpProblem, LpVariable, LpMinimize, lpSum
import matplotlib.pyplot as plt
from LP4SingleCurve import LP4SingleCurve

# load the community data
community_data = pd.read_excel('D:/Skool Staff/Programming/IoT_Coursework/IMSE7143-IoT2024-CW1/IMSE7143CW1Input.xlsx')
# load the abnormal curves
abnormal_curves = pd.read_csv('D:/Skool Staff/Programming/IoT_Coursework/Data/abnormal_curves.csv')
#use the LP4SingleCurve to do the linear programming for all the abnormal curves
for index in range(abnormal_curves.shape[0]):
    LP4SingleCurve(index,abnormal_curves,community_data)

















# #get the prices
# prices = abnormal_curves.iloc[0, :]  # 假设第0行是异常曲线的电价

# # 初始化一个模型
# model = LpProblem("Minimize_Electricity_Cost", LpMinimize)

# # 定义决策变量: 每个任务每小时的用电量
# power_vars = {}



# for idx, row in community_data.iterrows():
#     user_task = row['User & Task ID']
#     start_time = row['Ready Time']
#     end_time = row['Deadline']
#     max_power = row['Maximum scheduled energy per hour']
#     total_power = row['Energy Demand']

#     # 对每个任务，在每个小时分配一个用电量
#     for hour in range(start_time, end_time + 1):
#         power_vars[(user_task, hour)] = LpVariable(f"Power_{user_task}_{hour}", 
#                                                    lowBound=0, 
#                                                    upBound=max_power, 
#                                                    cat='Continuous')

# # 目标函数：最小化电费
# for idx0,row0 in community_data.iterrows():
#     user_task=row0['User & Task ID']
#     for hour in range(row0['Ready Time'],row0['Deadline']+1):
#         model+=lpSum(power_vars[(user_task, hour)]*prices[hour])
        
# # 约束：每个任务的总用电量
# for idx1, row1 in community_data.iterrows():
#     user_task = row1['User & Task ID']
#     total_power = row1['Energy Demand']
    
#     # 每个任务的总电量等于其需求
#     model += lpSum(power_vars[(user_task, hour)] for hour in range(row1['Ready Time'],row1['Deadline']+1)) == total_power, f"TotalPower_{user_task}"

# # 约束：每个任务每小时的用电量不能超过最大用电量
# for idx, row in community_data.iterrows():
#     user_task = row['User & Task ID']
#     start_time = row['Ready Time']
#     end_time = row['Deadline']
#     max_power = row['Maximum scheduled energy per hour']
    
#     for hour in range(start_time, end_time + 1):
#         model += power_vars[(user_task, hour)] <= max_power, f"MaxPower_{user_task}_{hour}"

# # 求解模型
# model.solve()

# total_power_per_hour=[0]*24

# # 输出结果
# if model.status == 1:
#     print("Optimal solution found!")
#     for user_task in community_data['User & Task ID']:
#         for hour in range(24):
#             if (user_task, hour) in power_vars:
#                 total_power_per_hour[hour]+=power_vars[(user_task,hour)].varValue
#                 print(f"{user_task} at hour {hour} uses {power_vars[(user_task, hour)].varValue} kWh")
# else:
#     print("No optimal solution found.")

# plt.figure(figsize=(10, 6))
# plt.bar(range(24), total_power_per_hour, color='skyblue')
# plt.xlabel('Hour of the Day')
# plt.ylabel('Total Power Usage (kWh)')
# plt.title('Total Power Usage over 24 Hours for the Community')
# plt.xticks(range(24))
# plt.grid(True, linestyle='--', alpha=0.7)
# plt.show()