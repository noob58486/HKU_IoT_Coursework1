#This is a function used to do the linear programming for a single curve

import pandas as pd
from pulp import LpProblem, LpVariable, LpMinimize, lpSum
import matplotlib.pyplot as plt
#seal the LP for single price curve as a function
def LP4SingleCurve(PriceIndex,abnormal_set,community_set):
    prices=abnormal_set.iloc[PriceIndex,:]
    #initiate a model
    model=LpProblem('Electricity_cost',LpMinimize)
    #define the electricity usage per hour for each task as the vars
    power_vars={}
    for idx,row in community_set.iterrows():
        user_task=row['User & Task ID']
        start_time=row['Ready Time']
        end_time=row['Deadline']
        max_power=row['Maximum scheduled energy per hour']
        total_power=row['Energy Demand']
        #configure the power usage per hour each task
        #the power usage per hour should be larer or equal to 0 and no more than the max power usage
        for hour in range(start_time,end_time+1):
            power_vars[(user_task,hour)]=LpVariable(f"Power_{user_task}_{hour}",lowBound=0,upBound=max_power,cat='Continuous')
    
    #define the target function
    total_cost = 0
    for idx0, row0 in community_set.iterrows():
        user_task = row0['User & Task ID']
        for hour in range(row0['Ready Time'], row0['Deadline'] + 1):
            total_cost += power_vars[(user_task, hour)] * prices[hour]
    model += total_cost
#power usage per hour*correspoding price and add up
    
    #add the constraint: total power usage for each task=total power requirement
    for idx1,row1 in community_set.iterrows():
        user_task=row1['User & Task ID']
        total_power=row1['Energy Demand']
        #add the constraint
        model+=lpSum(power_vars[(user_task,hour)] for hour in range(row1['Ready Time'],row1['Deadline']+1))==total_power,f"total_power_{user_task}"
    
    #add the constraint: power usage per hour each task is no more than max power usage per hour
    for idx2,row2 in community_set.iterrows():
        user_task=row2['User & Task ID']
        start_time=row2['Ready Time']
        end_time=row2['Deadline']
        max_power=row['Maximum scheduled energy per hour']
        
        for hour in range(start_time,end_time+1):
            model+=power_vars[(user_task,hour)]<=max_power,f"max_power_{user_task}_{hour}"
            
    #resolve the model
    model.resolve()
    
    total_power_per_hour=[0]*24#used to store the power usage per hour
    #output the result
    if model.status==1:
        print('Successfully solved')
        for user_task in community_set['User & Task ID']:
            for hour in range(24):
                if (user_task,hour) in power_vars:
                    total_power_per_hour[hour]+=power_vars[(user_task,hour)].varValue
                    print(f"{user_task} at hour {hour} uses {power_vars[(user_task, hour)].varValue} kWh")
    else:
        print('Error')
    #draw the bar graph and save    
    plt.figure(figsize=(10,6))
    plt.bar(range(24),total_power_per_hour,color='skyblue')
    plt.xlabel('Time')
    plt.ylabel('Power Usage(kWh)')
    plt.title('Power Usage over 24 Hour')
    plt.xticks(range(24))
    plt.grid(True,alpha=0.7)
    plt.savefig(f'D:\Skool Staff\Programming\IoT_Coursework\Data\BarGraphs\BarGraph{PriceIndex+1}.png',format='png',dpi=300)
    #plt.show()
                        