
# Medicare fraud detection
A machine learning based web application to help detect fraudulent practitioners among Medicare.

Check the notebooks for more details about data processing and model training/evaluation.
## Requirements

* Python 3.9+
* conda (to create the virtual environments)

## Usage 
#### Launching the app
* Make sure that the requirements are installed : 
```python
pip install requirements.txt
``` 
* Launch the app from terminal :
```
python app.py
``` 

![alt text](https://i.ibb.co/gMpTxzL/interface.png)
__It is very important that the CSV file respects a specific order of columns / variables :__
   
    1. Specialty
    2. State
    3. Total HCPCS
    4. Male Patients Count
    5. Average Age
    6. Total Services
    7. Total Patients
    8. Average Risk Score
    9. Charges Submitted
    10. Charges Paid 
#### Creating the virtual environments
* Make sure that conda is installed and run the following command :
```python
conda env create -f medicare-fraud-env.yml
``` 
* Activate the environment :
```python
conda activate medicare-fraud
``` 