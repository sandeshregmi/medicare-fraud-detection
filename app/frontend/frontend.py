#Streamlit FrontEnd UI

import io
import requests
import streamlit as st
import pandas as pd
import json
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from specs_states import states,specs

#Function that sends an HTTP request to FASTAPI's first end point (form)
def get_label(url,data):
    res = requests.post(url, json = data)
    print('Response time : '+str(res.elapsed.total_seconds())+' seconds')
    return res

#Function that sends an HTTP request to FASTAPI's second end point (file)
def get_labels(url,data):
    res = requests.post(url, data = data)
    print('File response time : '+str(res.elapsed.total_seconds())+' seconds')
    return res

#Function that converts user input to JSON in order to send the HTTP request
def format_data(gender,spec,state,tot_hcpcs,male_bene,avg_age,tot_serv,tot_bene,avg_risk_score,charges_subm,charges_payed):
    
    formated = {
        "spec": spec,
        "state": state,
        "gender": gender,
        "tot_hcpcs": tot_hcpcs,
        "male_bene": male_bene,
        "avg_age": avg_age,
        "tot_serv": tot_serv,
        "tot_bene": tot_bene,
        "avg_risk_score": avg_risk_score,
        "charges_subm": charges_subm,
        "charges_payed": charges_payed
    }

    return formated

#Function that clears the form when the button is clicked
def clear():

    st.session_state['gender']='Male'
    st.session_state['spec']='Addiction Medicine'
    st.session_state['state']='AE'
    st.session_state['tot_hcpcs']=0
    st.session_state['male_bene']=0
    st.session_state['avg_age']=0
    st.session_state['tot_serv']=0
    st.session_state['tot_bene']=0
    st.session_state['avg_risk_score']=0
    st.session_state['charges_subm']=0
    st.session_state['charges_payed']=0
    

#Function that clears the history when the button is clicked
def clear_hist():
    st.session_state.history =pd.DataFrame(data=one_line)

#Function that highlights the fraudulent providers rows
def highlight(df,column): 
    fraud = pd.Series(data=False, index=df.index)
    fraud[column] = df.loc[column] == 'Potential Fraud'
    return ['background-color: #ED2939' if fraud.any() else '' for v in fraud]

#Function that checks string/numeric type + positive values
def check_num_str(df):
    val = 1
    cols = df.columns
    str_cols = [cols[0],cols[1],cols[2]]
    num_cols = [col for col in cols if col not in str_cols]
    
    #Check string values
    for col in str_cols:
        if(not(is_string_dtype(df[col]))):
            st.warning("Error ! '"+ col+"'" +" has to be of type string!")
            val = 0
    #Check numeric values
    for col in num_cols:
        if(not(is_numeric_dtype(df[col]))):
            st.warning("Error ! '"+ col+"'" +" has to be of type numeric")
            val = 0
        #Check positive values
        elif(min(df[col])<0):
            st.warning("Error ! '"+ col+"'" +" values have to be positive")
        
    
    return val

#Function that checks if the dataframe format is correct and ready to be sent to API
def check_df(df): 
    col=df.columns
    int_cols = [col[3],col[4],col[6],col[7]]
    val = 0
    specs_low=[x.lower() for x in specs]
    states_low=[x.lower() for x in states]
    if(check_num_str(df)) :
        val = 1
        #Check speciality values
        if (not(all(elem in specs_low for elem in list(df[col[0]].str.lower())))):
            st.warning("Error ! Check '"+col[0]+"' values")
            val = 0

        #Check state values
        if (not(all(elem in states_low for elem in list(df[col[1]].str.lower())))):
            st.warning("Error ! Check '"+col[1]+"' values")
            val = 0

        #Check gender values
        if (not(all(elem in ['m','male','f','female'] for elem in list(df[col[2]].str.lower())))):
            st.warning("Error ! Check '"+col[2]+"' values")
            val = 0
        
        #Check integer values
        for col in int_cols:
            if(not((df[col] % 1  == 0).all())):
                st.warning("Error ! '"+ col+"'" +" has to be of type integer")
                val=0    
    
    return val

#Function that checks if the form format is correct and ready to be sent to API
def check_form(tot_hcpcs,male_bene,tot_bene,tot_serv):
    val = 1
    
    
    int_cols={'Total HCPCS':tot_hcpcs,
    'Male Patients Count':male_bene,
    'Total Patients ':tot_bene,
    'Total Services':tot_serv}
    #Check integer values
    for f in int_cols.keys():
        if(not((int_cols[f] % 1  == 0))):
                st.warning("Error ! '"+f+"'" +" has to be of type integer")
                
                val=0

    return val

#One dataframe row
one_line={"status":[],'spec':[],'state':[],'gender':[],'tot_hcpcs':[],'male_bene':[],'avg_age':[],'tot_serv':[],'tot_bene':[],'avg_risk_score':[],'charges_subm':[],'charges_payed':[]}

#History dataframe
history=pd.DataFrame(data=one_line)

if 'history' not in st.session_state:
    st.session_state['history'] = history

#Set page title
st.title('Medicare fraud detection')


#First container (manually enter a practitioner)
with st.container():
    
    st.subheader('Enter the practitioner annual details :')
    col1, col2 = st.columns([1,1],gap='small')

    #User input
    with col1:
        st.write('\n')
        st.write('\n')
        st.write('')
        gender = st.radio("Gender :",('Male', 'Female'),horizontal=True,key='gender')
        spec=st.selectbox('Specialty :',options=sorted(specs),key='spec')
        state=st.selectbox('State :',options=sorted(states),key='state')
        tot_hcpcs = st.number_input("Total HCPCS :",key='tot_hcpcs',min_value=0.00)
        male_bene = st.number_input("Male Patients Count :",key='male_bene',min_value=0.00)
        
        

    with col2:
        avg_age = st.number_input("Average Age :",key='avg_age',min_value=0.00)
        tot_serv = st.number_input("Total Services :",key='tot_serv',min_value=0.00)
        tot_bene = st.number_input("Total Patients :",key='tot_bene',min_value=0.00)
        avg_risk_score = st.number_input("Average Risk Score :",key='avg_risk_score',min_value=0.00)
        charges_subm = st.number_input("Charges Submitted :",key='charges_subm',min_value=0.00)
        charges_payed = st.number_input("Charges Paid :",key='charges_payed',min_value=0.00)
    
    col5,col6,col7,col8,col9 = st.columns(5,gap='small')
    
    #Buttons
    with col5:
        pass
    with col6:
       
        submitted = st.button("Submit")
    with col7:
        
        st.button("Clear",on_click=clear)
    with col8:
        
        hist = st.button("History")
    with col9:
        pass
    
    #Send request to API
    url1 =  "http://localhost:8000/Fraud_detection_single"
    if(submitted):
        if(check_form(tot_hcpcs,male_bene,tot_bene,tot_serv)):
            with st.spinner('Processing ...'):
                #Format data
                data_pract= format_data(gender,spec,state,tot_hcpcs,male_bene,avg_age,tot_serv,tot_bene,avg_risk_score,charges_subm,charges_payed)
                #Get label
                res = get_label(url1,data_pract)
                res=res.json()
                label=res['label']
                
                if(label=='Potential Fraud'):
                    fraud =  st.error(label)
                
                elif (label=='Legitimate') :
                    legit =  st.success(label)
                
                #Store Response in state variable
                one_line['status']=label
                for key in data_pract.keys():
                    one_line[key]=data_pract[key]
                
                #Concat history rows
                st.session_state.history=pd.concat([st.session_state.history, pd.DataFrame.from_dict(one_line,orient='index').T],ignore_index=True)
                
            
    #History
    if(hist):
        #Show history
        df_tmp = st.session_state.history.style.apply(highlight, column='status',axis=1)
        st.write(df_tmp)
        if(st.session_state.history.shape[0]!=0):
            #History buttons
            col66,col77,col99,col90 = st.columns(4,gap='small')
            with col66:
                pass
            with col77:
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df_tmp.to_excel(writer,index=False)
                    
                st.download_button(label="Download",data=buffer,file_name='History.xlsx',mime="application/vnd.ms-excel")
            
            with col99:
                
                st.button(label='Clear History',on_click=clear_hist)
                    
            
st.write()
st.markdown("""---""")
st.write()

#Second container (Upload File)
with st.container():
    st.subheader('Upload your file: ')
    #Upload box
    uploaded_file = st.file_uploader("Choose a file : ",['csv'],key='upload')
    
    #Button
    col9, col10, col11,col12,col13 = st.columns(5)
    with col9:
        pass
    with col10:
        pass
    with col11:
        uploaded = st.button("Process")
    with col12:
        pass
    with col13:
        pass
    url2 =  "http://localhost:8000/Fraud_detection_multiple"
    if(uploaded):
        with st.spinner('Processing ...'):
            if uploaded_file is not None:
                
                #Read file
                df=pd.read_csv(uploaded_file,index_col=False)
                
                if(check_df(df)):
                    #Format data
                    df.columns = ['spec', 'state', 'gender', 'tot_hcpcs','male_bene','avg_age','tot_serv','tot_bene','avg_risk_score','charges_subm','charges_payed']
                    data_frame = json.dumps(df.to_dict(orient='list'))
                    #Get labels
                    res = get_labels(url2,data_frame)
                    res=res.json()
                    labels=res['labels']

                    #Show new dataframe
                    df2=df.copy()
                    df2.insert(loc=0, column='status', value=labels)
                    df2=df2.reset_index(drop=True)                
                    df3=df2.copy()
                    df2=df2.style.apply(highlight, column='status',axis=1)
                    st.write(df2)
                    #Nb of potential fraud detected
                    st.error(str(sum(df3['status']=='Potential Fraud')) +' Potential fraud detected !!')
                    col14, col15, col16 = st.columns(3)
                    with col14:
                        pass
                    with col16:
                        pass
                    with col15:
                        #Download as Excel
                        buffer2 = io.BytesIO()
                        with pd.ExcelWriter(buffer2, engine='xlsxwriter') as writer:
                            df2.to_excel(writer,index=False)
                        st.download_button(label="Download & Clear",data=buffer2,file_name='Processed_'+uploaded_file.name[:-3]+'xlsx',mime="application/vnd.ms-excel")
                        
                       
                        
                
        
                








        