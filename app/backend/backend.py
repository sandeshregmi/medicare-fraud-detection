#FASTAPI Backend RESTAPI 

import pandas as pd
import numpy as np
from fastapi import FastAPI
from joblib import load
import os
from pathlib import Path
import uvicorn
from pydantic import BaseModel,StrictStr

class DataFrame(BaseModel):
    """Dataframe that contains the practitioner details"""
  
    spec : list 
    state : list
    gender : list
    tot_hcpcs : list
    male_bene : list
    avg_age : list
    tot_serv : list
    tot_bene : list
    avg_risk_score : list
    charges_subm : list
    charges_payed : list

class Practitioner(BaseModel):
    """Class which describes Practitioner's informations """
  
    spec : StrictStr
    state : StrictStr
    gender : StrictStr
    tot_hcpcs : int
    male_bene : int
    avg_age : float
    tot_serv : int
    tot_bene : int
    avg_risk_score : float
    charges_subm : float
    charges_payed : float

#set root directory
path = Path(__file__)
root_dir = path.parent.parent.parent.absolute()

# Load Trained 'Random Forest Model'
model = load(str(root_dir)+'/models/Random_forest.pkl')

# Read one line from dataframe to get the columns names
first_line = pd.read_csv(str(root_dir)+'/app/backend/columns.csv')
#Function that converts gender to numeric
def conv_gender(gnd):
    if (gnd.lower() in ["m","male"]):
        return 1
    return 0

#Function that converts user input in order to be passed to the model for the prediction
def convert_input(gender,tot_hcpcs,male_bene,avg_age,tot_serv,tot_bene,avg_risk_score,charges_subm,charges_payed,spec,state):
    #Get columns (lower)
    cols=first_line.columns
    lower_cols = [col.lower() for col in cols]

    #Initiate the vector
    new_input = np.zeros((1,146))
    
    #Convert 'gender'
    new_gender = conv_gender(gender)

    #Put the input variables in the correct order
    new_input[:,0:9]=[new_gender,tot_hcpcs,male_bene,avg_age,tot_serv,tot_bene,avg_risk_score,charges_subm,charges_payed]
    spec,state=spec.lower(),state.lower()
    spec,state='rndrng_prvdr_type_'+spec,'rndrng_prvdr_state_abrvtn_'+state
    idx_spec,idx_state=lower_cols.index(spec),lower_cols.index(state)
    new_input[:,idx_spec],new_input[:,idx_state]=1,1

    #Convert input to dataframe
    new_input = pd.DataFrame(data=new_input,columns=cols)

    return new_input 

#Function that returns model's output
def predict(new_input):
    #Get prediction from converted input
    pred = model.predict(new_input)

    #Convert prediction to string
    label = 'Potential Fraud' if pred==1 else 'Legitimate'
    
    return label

#Initiate FastAPI applicaition
app = FastAPI()


#Index route, opens automatically on http://127.0.0.1:8000
#Health check
@app.get('/')
def root():
    return {"message" : "Fraud Detection API"}


@app.post('/Fraud_detection_single')
#First endpoint : gets user input from form and returns model's prediction 
def response(pract : Practitioner):

    #user input
    spec=pract.spec
    state=pract.state
    gender=pract.gender
    tot_hcpcs=pract.tot_hcpcs
    male_bene=pract.male_bene
    avg_age=pract.avg_age
    tot_serv=pract.tot_serv
    tot_bene=pract.tot_bene
    avg_risk_score=pract.avg_risk_score
    charges_subm=pract.charges_subm
    charges_payed=pract.charges_payed

    #Convert user input to dataframe
    new_input = convert_input(gender,tot_hcpcs,male_bene,avg_age,tot_serv,tot_bene,avg_risk_score,charges_subm,charges_payed,spec,state)
    #Predict the label of converted input 
    pred = predict(new_input)
    print(pred)
    return {"label" : pred}

@app.post('/Fraud_detection_multiple')
#seconde endpoint : gets uploaded user file (csv) and returns model's predictions
def response(df : DataFrame):
    #list to store all labels
    labels=[]

    spec=df.spec
    state=df.state
    gender=df.gender
    tot_hcpcs=df.tot_hcpcs
    male_bene=df.male_bene
    avg_age=df.avg_age
    tot_serv=df.tot_serv
    tot_bene=df.tot_bene
    avg_risk_score=df.avg_risk_score
    charges_subm=df.charges_subm
    charges_payed=df.charges_payed
    
    #loop over file rows
    for i in range(len(spec)):
        #Convert each row to dataframe
        new_input = convert_input(gender[i],tot_hcpcs[i],male_bene[i],avg_age[i],tot_serv[i],tot_bene[i],avg_risk_score[i],charges_subm[i],charges_payed[i],spec[i],state[i])
        #Append predicted labels to list
        labels.append(predict(new_input))
   
    return {"labels" : labels}
    
if __name__ == '__main__':

    uvicorn.run(app, host='127.0.0.1', port=8000)
