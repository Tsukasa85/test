from classes import *


#all the information you need to get started should be here.

############### Data Containers ###############
#Assets=[]  #hold all assets that user owns
#Liabilities


############### Information collected from the web page ###############
### BASIC QUESTIONS ###
#"What is your monthly expense? (bare necessaties)"
basicInfo_monthyExpense=2000
basicInfo_haveEmergencyFund=True
basicInfo_emergencyFund=10000
basicInfo_grossIncome=70000

### Liabilities ###
#"Do you have any loans?
#Liability_1_name="Car"
#Liability_1_payment = 350
#Liability_1_numPaymentLeft = 12 # month
liabilities_interest = [3.5] #0.01=1%


### ASSETS ###

#401k
_401k_employerOffer = "True" #(T/F/IDK)
_401k_have = "True"  #(T/F/IDK)
_401k_employerMatch = "True" #(T/F/IDK)
_401k_matchPercent = 100
_401k_uptoPercent = 5
_401k_currentContribution = 1200 #$. Do % later. check to see if it's maxed
_401kArray=[_401k_employerOffer, _401k_have, _401k_employerMatch, _401k_matchPercent, _401k_uptoPercent, _401k_currentContribution]

#HSA
_HSA_haveHighDeductible="True" #(T/F/IDK) # check if you can have it
_HSA_haveHSA="True" #(T/F/IDK) #ask only if haveHighDeductible is True
_HSA_contribution=3300 #$. Do % later.  Check to see if it's maxed out.  Research if employer contribution counts too.
_HSA_SingleOrFamily="Single"
_HSAArray=[_HSA_haveHighDeductible, _HSA_haveHSA, _HSA_contribution, _HSA_SingleOrFamily]

#IRA
_IRA_contribute="True" #(T/F/IDK)
_IRA_contribution=5500 #check if maxed
_IRA_RothOrTraditional="Roth" #check against max Roth contribution
_IRAArray=[_IRA_contribute, _IRA_contribution, _IRA_RothOrTraditional]

#Taxable income
_taxable_have=True #T/F/IDK
_taxable_contribution=0 #check how much tax benefit you could have
_taxableArray=[_taxable_have, _taxable_contribution]

############### Run stuff on the backend ###############

basic=Basic([basicInfo_monthyExpense, basicInfo_haveEmergencyFund, basicInfo_emergencyFund, basicInfo_grossIncome])
liabilities=Liability(liabilities_interest)
assets=Asset(_401kArray, _HSAArray, _IRAArray, _taxableArray)
model=Model(basic,liabilities,assets)
model.run()
model.displayResults()

############### Display results on front end ###############
#recommendation:
#	"Payoff your credit cards debt"
#	"Pay the minimum amount for all loans"
#	"Work on your emergency funds.  It should be..."
#model.displayResults()

#	"Here is the prioritized list of fund you should put money in"
#	"401k match up", "Xtra to loan (>7%)", "HSA", "IRA roth",  "Taxed Investment", "Xtra to loan (<5%)"
#	List out max possible contribution amount










