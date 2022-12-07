# U.S. Medicaid Opioid Prescription Claims and Rate Mapping and Trends
### Author: Katherine Meng

Created as a result of Chase Romano’s Visual Analytical course in the Healthcare Informatics Analytics master’s program at the University of North Carolina Charlotte, this app allows health care users and government policy makers in the United States to monitor and analyze the Medicaid opioid prescription claims and claim rates in their state from 2013 to 2020.

To view the live app go to https://opioid-prescription-trend-rate.streamlit.app/

### Healthcare Problem Context
Opioid abuse and overdose have been a major concern in the United States since the 1990s. In 2017, U.S. Department of Health and Human Services declared a public health emergency to address national opioid crisis. Medicaid, a joint Federal-State medical assistance program in the U.S. for low-income individuals and families, has spent significantly high cost each year on opioid-based drugs for its beneficiaries. The purpose of this app is to give the users and policy makers a tool to visualize Medicaid opioid prescription claims and claim rates.

### Data Source
The dataset used for this app, Medicaid Opioid Prescription Rates by Geography (2013 - 2020), was public information downloaded from the website of the U.S. Centers for Medicare and Medicaid Services (CMS). It provides the Medicaid opioid prescription claim and rate data in each state of the United States from year 2013 to 2020. The dataset can be retrieved from the link below: 

https://data.cms.gov/summary-statistics-on-use-and-payments/medicare-medicaid-opioid-prescribing-rates/medicaid-opioid-prescribing-rates-by-geography/data

### Preparation of Data
Preparation of data:
- •	Identify variables to be used
•	Check for missing values
•	Check for consistency (spelling, units, etc.)
•	Add longitudinal and latitudinal data points to allow Streamlit geographic mapping
•	Add state abbreviation as state codes to allow plotly geographic plotting
•	Separate dataset into different data sheets based on different Medicaid plans (Fee for Service, Managed Care, All Plans)

### Future Improvement Recommendations
The app can be improved in the following areas:
•	The trend can be select for each year and for each individual state
•	The trends can be easily compared from state to state
•	The numbers of claims and claim rates can be correlated 

