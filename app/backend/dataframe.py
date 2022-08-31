from pydantic import BaseModel, StrictInt, StrictStr

# DataFrame

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