[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mohamed-lahna-medicare-fraud-detection-streamlitmain-dep-5q9z51.streamlitapp.com/)

# Medicare fraud detection
A machine learning based web application to help detect fraudulent practitioners among Medicare.

* Check the notebooks for more details about data processing and model training/evaluation.

## Requirements
* Python 3.9+
* conda (to create the virtual environments)

## Usage 
#### Launching the app
* Make sure that the requirements are installed : 
```python
pip install -r requirements.txt
``` 
* Launch the app from terminal :
```
python app.py
``` 

![alt text](https://i.ibb.co/t2RpCwH/222.png)


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

#### Creating the virtual environment
* Make sure that conda is installed and run the following command :
```python
conda env create -f medicare-fraud-env.yml
``` 
* Activate the environment :
```python
conda activate medicare-fraud
``` 
## Data used
### Overview
The dataset used describes the services and procedures that health care professionals provide to Medicare beneficiaries. The records in the dataset contain various provider-level attributes, such as National Provider Identifier (NPI), first and last name, gender, address, etc.
In addition, the records contain information that describes a provider's Medicare activity in a given year. Examples include: the procedure performed, the average fee submitted to Medicare, the average amount paid by Medicare, and the location of service.

This dataset is aggregated at the NPI level, the identifier of a provider, and contains information for the years 2016 through 2019 with over one million records and 73 variables for each year, which makes this database an excellent candidate for data analysis and machine learning.

The Medicare provider fraud labels are identified using LEIE data, LEIE is maintained by the OIG in accordance with sections 1128 and 1156 of the Social Security Act and is updated monthly. The OIG has the authority to exclude providers from federally funded health care programs for various reasons. Excluded individuals cannot receive payment from federal health programs for any services, and must apply for reinstatement once their exclusion period has expired. The current LEIE data format contains 18 attributes that describe the provider and the reason for the exclusion.
### Data sampling
After data processing and labeling , the final dataset includes information on 4,419,977 practitioners, of which 1,276 are fraudulent, which represents a little over 0.03% of the total workforce.

The fraud rate (0.03%) does not reflect reality (10% worldwide), therefore it is necessary to select a sample of the negative class (population) to increase the fraud rate up to 10%.
The sample was selected using random sampling, and statistical tests were used to ensure that it was not biased.

Check the notebooks for more details.