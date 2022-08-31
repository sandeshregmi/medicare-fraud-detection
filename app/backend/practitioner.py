from pydantic import BaseModel, StrictInt, StrictStr

#Class which describes Practitioner's informations 
  

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