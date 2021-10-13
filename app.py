from flask import Flask, jsonify, request,render_template
from sklearn.preprocessing import StandardScaler
import pandas as pd
import joblib
import pickle
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('table.html')

@app.route("/predict-age", methods=['GET'])
def predict_age():
    test_data = pd.read_csv(r"Test_data.csv")
    test_data.drop(columns=["Unnamed: 0"],inplace=True)
    test_data=test_data.drop_duplicates(subset="device_id",keep="first")
    age_model = pickle.load(open('finalized_model_age.pkl', 'rb'))
    
    test_data["Total_No_events"]=StandardScaler().fit_transform(test_data[["Total_No_events"]])
    test_data["Change_in_LatLong"]=StandardScaler().fit_transform(test_data[["Change_in_LatLong"]])
    test_data["longitude_median"]=StandardScaler().fit_transform(test_data[["longitude_median"]])
    test_data["latitude_median"]=StandardScaler().fit_transform(test_data[["latitude_median"]])
    x_test=test_data.drop(columns=["gender","age","group_train","super_category","train_test_flag","device_id","phone_brand"])
    age_predict = age_model.predict(x_test.values)
    test_data["predicted_age"]= age_predict
    campain4=test_data[test_data["predicted_age"]<25]["device_id"][:5].to_list()
    campain5=test_data[test_data["predicted_age"].between(24,32)]["device_id"][:5].to_list()
    campain6=test_data[test_data["predicted_age"]>32]["device_id"][:5].to_list()
    headings=("campaign","device_id","age")
    data1=[]
    for i in np.unique(campain4):
        temp=(4,i,"Bundled smartphone offers for the age group [0-24]")
        data1.append(temp)
    for i in np.unique(campain5):
        temp=(5,i,"Special offers for payment wallet offers [24-32]")
        data1.append(temp)
    for i in np.unique(campain6):
        temp=(6,i,"Special cashback offers for Privilege Membership [32+]")
        data1.append(temp)
    data=tuple(data1)
    return render_template('table.html',headings=headings,data=data)

@app.route("/predict-gender", methods=['GET'])
def predict_gender():
    test_data = pd.read_csv('Test_data.csv')
    #gender_model = joblib.load('model/gender_prediction.pkl')
    test_data.drop(columns=["Unnamed: 0"],inplace=True)
    test_data=test_data.drop_duplicates(subset="device_id",keep="first")
    gender_model = pickle.load(open('finalized_model_gender.pkl', 'rb'))

    test_data["Total_No_events"]=StandardScaler().fit_transform(test_data[["Total_No_events"]])
    test_data["Change_in_LatLong"]=StandardScaler().fit_transform(test_data[["Change_in_LatLong"]])
    test_data["longitude_median"]=StandardScaler().fit_transform(test_data[["longitude_median"]])
    test_data["latitude_median"]=StandardScaler().fit_transform(test_data[["latitude_median"]])
    x_test=test_data.drop(columns=["gender","age","group_train","super_category","train_test_flag","device_id","phone_brand"])
    gender_predict = gender_model.predict_proba(x_test)
    y_pred=[1 if x >0.759951 else 0 for x in gender_predict[:, 1]]
    test_data["predicted_gender"]=y_pred
    headings=("campaign","device_id","Description")
    campain1=test_data[test_data["predicted_gender"]==0]["device_id"][:5].to_list()
    campain2=test_data[test_data["predicted_gender"]==0]["device_id"][5:10].to_list()
    campain3=test_data[test_data["predicted_gender"]==1]["device_id"][:5].to_list()
    data1=[]
    for i in np.unique(campain1):
        temp=(1,i,"Specific personalised fashion-related campaigns targeting female customers")
        data1.append(temp)
    for i in np.unique(campain2):
        temp=(2,i,"Specific cashback offers on special days (International Women’s Day etc) targeting female customers")
        data1.append(temp)
    for i in np.unique(campain3):
        temp=(3,i,"Personalised call and data packs targeting male customers")
        data1.append(temp)
    data=tuple(data1)
    return render_template('table.html',headings=headings,data=data)

if __name__ == "__main__":
    app.run(host='0.0.0.0')