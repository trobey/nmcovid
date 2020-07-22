# New Mexico Covid model

A Coronovirus SIR model for New Mexico

## Description

This is a demo of a New Mexico Covid model in Python Mesa.  There is not much calibration attempted and there is a lot that could be improved.  But it does start to show the impact of the geography and distribution of population on the spread of the coronavirus within the state of New Mexico.  

Mesa is a Python library for agent-based modeling.  This model is a Susceptible - Infected - Recovered (SIR) that is rather basic.  The agents are distributed by county so that it matches the actual distribution of the population but does not capture anything below the count level.  Travel of agents uses a uniform distribution with an average of 13 miles for work/school and 15 miles for community (shopping, church, etc.).  This understates travel for longer distances although these trip are a small percentage of the overall travel by car.

![Coronovirus outbreak modeled for Las Cruces](/nmcovid.png)

There are significant public lands in New Mexico that could concentrate population in some counties and also provide additional geographical barriers to the spread of the virus. The model does not take into account congregate facilities in rural areas (jails, nursing homes, etc.) where population density within the facility allows for outbreaks even though the overall community may not have enough population density to sustain a prolonged outbreak.  Also, the tribal areas have multigenerational households and close knit communities with limited stores that make them more susceptible to outbreaks than the model captures.

There are parts of the state where outbreaks in the model quickly die out.  Real outbreaks in these areas may not die out so easily but it should be easier to get outbreaks in these regions under control.  The main concern in these outlying areas is congregate facilities and tribal areas.  The virus spreads very quickly in the Albuquerque and Las Cruces areas.  Outbreaks in these parts of the state should be much more difficult to get under control.  The Albuquerque and Las Cruces areas are separated by geography such that it is difficult for outbreaks to spread from one to the other.  There are other areas in the middle such as the northern Rio Grande valley and southeastern New Mexico that spread of the virus may or may not die out.  Midland and Odessa are not included in the model since they are in Texas but they may influence the spread of the virus in southeastern New Mexico.

## Instructions

Install Python 3 and download the New Mexico Covid model.

* pip install mesa

* cd nmcovid

The run.py file should be in the current directory

* pip install -r requirements.txt

This should install Mesa if you did not install it in the first step.

* mesa runserver
