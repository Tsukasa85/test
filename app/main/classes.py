class Model:

   global requiredEmergencyDuration
   requiredEmergencyDuration=3 #months * monthly expense

   def __init__(self,basic,liabilities,assets):
      self.basic = basic
      self.liabilities = liabilities
      self.assets = assets

   def run(self):
      i=1 #recommendation ranking counter
      #logic to make the recommendations
      display=["#### Results ####"]
      display.append(str(i)+": "+"Payoff your credit card debts if any. Or other super high interst loans.")
      i+=1

      if (len(self.liabilities)>0): 
         display.append(str(i)+": "+"Pay the minimum amount for all loans.")
         i+=1

      if (len(self.assets)==0):
         display.append(str(i)+": "+"Create an emergency fund of: "+str(self.basic.monthlyExpense*requiredEmergencyDuration))
         i+=1
      else:
         if(self.assets[0].balance<(self.basic.monthlyExpense*requiredEmergencyDuration)):
            display.append(str(i)+": Add more funds to emergency fund.")
            i+=1
            display.append("It should be at: $"+str(self.basic.monthlyExpense*requiredEmergencyDuration))
            display.append("It is currently at: $"+str(self.assets[0].balance))

      if (self.basic.enable401k):
         if(self.basic.enable401kMatchup>0):
            display.append(str(i)+": Contribute to 401k up to company match up portion")
            i+=1

      for liability in self.liabilities:
         if(liability.interest>=0.07):
            display.append(str(i)+": Payoff your high interest (>7%) loans.")
            i+=1

      display.append(str(i)+": Contribute to HSA account.")
      i+=1

      for liability in self.liabilities:
         if((liability.interest>=0.04) and (liability.interest<0.07)):
            dispaly.append(str(i)+": Payoff your loans wiht interest rates of >4%.")
            i+=1

      display.append(str(i)+": Contribute to IRA account (outside of 401k).")
      i+=1

      display.append(str(i)+": Contribute to 401k account to maximum allowable.")
      i+=1

      display.append(str(i)+": Contribute to taxable investments.")
      i+=1

      for liability in self.liabilities:
         if((liability.interest>=0) and (liability.interest<0.04)):
            display.append("Continue to payoff your loans wiht interest rates of <4%"+" with the standard payment schedule.")



      self.display=display

   def displayResults(self):
      #i=0
      for line in self.display:
         #if(i>0):
         #   line=str(i)+":"+line
         #i+=1
         print line



class Basic:
   def __init__(self,monthlyExpense,enable401k,enable401kMatchup):
      self.monthlyExpense=monthlyExpense
      self.enable401k=enable401k
      self.enable401kMatchup=enable401kMatchup

class Liability:
   def __init__(self,interest):
      self.interest=interest

class Asset:
   def __init__(self, balance):
      self.balance = balance

