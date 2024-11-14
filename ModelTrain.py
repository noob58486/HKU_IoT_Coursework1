from txt2csv import txt2csv#format converting function
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix

#convert the datasets into csv format
train_txt_path='D:\Skool Staff\Programming\IoT_Coursework\IMSE7143-IoT2024-CW1/TrainingData.txt'
train_csv_path='D:\Skool Staff\Programming\IoT_Coursework\Data/train.csv'

txt2csv(train_txt_path,train_csv_path)

test_txt_path='D:\Skool Staff\Programming\IoT_Coursework\IMSE7143-IoT2024-CW1/TestingData.txt'
test_csv_path='D:\Skool Staff\Programming\IoT_Coursework/Data/test.csv'

txt2csv(test_txt_path,test_csv_path)

#load the data
data=pd.read_csv(train_csv_path)

#split the train set to features and label
X=data.drop(columns='status')
y=data['status']

#split the set to train and validation
X_train,X_val,y_train,y_val=train_test_split(X,y,test_size=0.2,random_state=42)

#create the lgb dataset
train_data=lgb.Dataset(X_train,label=y_train)
val_data=lgb.Dataset(X_val,label=y_val,reference=train_data)

#set the lgb parameters
params={
    'objective':'binary',
    'metric':'binary_logloss',
    'boosting_type':'gbdt',
    'num_leaves':31,
    'learning_rate':0.05,
    'feature_fraction':0.9
}

#train the model
model=lgb.train(params,train_data,valid_sets=[val_data],num_boost_round=1000)

#read the test set
test_set=pd.read_csv(test_csv_path)

#test the model on the validation set
y_val_pred=model.predict(X_val)
y_val_pred_binary=[1 if x>0.5 else 0 for x in y_val_pred]

#calculate the metrics
accuracy = accuracy_score(y_val, y_val_pred_binary)
report = classification_report(y_val, y_val_pred_binary)
conf_matrix = confusion_matrix(y_val, y_val_pred_binary)
#print the metrics
print("模型准确率: {:.2f}%".format(accuracy * 100))
print("\n分类报告:\n", report)
print("混淆矩阵:\n", conf_matrix)
#predict the test set with our model
preds=model.predict(test_set)
#convert the prediction probability to binary labels
preds_binary=[1 if x>0.5 else 0 for x in preds]
#add a label colunm for test set
test_set['label']=preds_binary
#output the test_result.txt
test_set.to_csv('D:/Skool Staff/Programming/IoT_Coursework/Data/test_results.txt',sep=',',index=False,header=False)
#get the abnormal curves
abnormal_curves=test_set[test_set['label']==1]
abnormal_curves=abnormal_curves.drop(columns=['label'])
abnormal_curves.to_csv('D:/Skool Staff/Programming/IoT_Coursework/Data/abnormal_curves.csv', index=False)
#abnormal_curves.to_csv('D:/Skool Staff/Programming/IoT_Coursework/Data/abnormal_curves.txt',sep=',',index=False,header=False)
#print the results for test set
print('results:')
print(preds_binary)
#output the result to a txt file
results=pd.DataFrame({
    'Data ID':range(1,len(preds_binary)+1),
    'Prediction':preds_binary
})

results.to_csv('D:\Skool Staff\Programming\IoT_Coursework/Data/result.txt',sep='\t',index=False,header=False)
