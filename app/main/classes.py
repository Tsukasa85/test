class Model:

   global requiredEmergencyDuration
   requiredEmergencyDuration=3 #months * monthly expense

   def __init__(self,basic,liabilities,assets):
      self.basic = basic
      self.liabilities = liabilities
      self.assets = assets
      self.displayContents =[]
      self.inputSummary = []



   def createInputSummary(self):
      display=[]

      display.append("Basic")
      for stuff in self.basic.basicInfoArray:
         display.append(stuff)

      display.append("Liabilities")
      for stuff in self.liabilities.interestArray:
         display.append(stuff)

      display.append("Assets")
      for stuff in self.assets.g401kArray:
         display.append(stuff)

      for stuff in self.assets.HSAArray:
         display.append(stuff)

      for stuff in self.assets.IRAArray:
         display.append(stuff)

      for stuff in self.assets.taxableArray:
         display.append(stuff)

      self.inputSummary+=display




   def run(self):
      i=1 #recommendation ranking counter
      #logic to make the recommendations
      display=[]
      display.append(str(i)+": "+"Continue to make your minimum expense payments.  This includes your minimum payments to loans.")
      i+=1

      #Emergency fund
      if (not self.basic.basicInfo_haveEmergencyFund):
         display.append(str(i)+": "+"Create an emergency fund of "+str(self.basic.basicInfo_monthyExpense*requiredEmergencyDuration))
         i+=1
      else:
         if(self.basic.basicInfo_emergencyFund<(self.basic.basicInfo_monthyExpense*requiredEmergencyDuration)):
            display.append(str(i)+": Add more funds to emergency fund.")
            i+=1
            display.append("It should be at: $"+str(self.basic.basicInfo_monthyExpense*requiredEmergencyDuration))
            display.append("It is currently at: $"+str(self.basic.basicInfo_emergencyFund))

      #high interest pay down
      for interest in self.liabilities.liabilities_interest:
         if (float(interest)>=15):
            display.append(str(i)+": "+"Pay off the loans with interest rate of 15 percent or higher.")
            i+=1
            break

      #401k
      if (self.assets.g401k_employerOffer=="True"):
         if (self.assets.g401k_have=="True"):
            if (self.assets.g401k_employerMatch=="True"):
               self.max401kMatch=(self.assets.g401k_uptoPercent/100.0)*(self.basic.basicInfo_grossIncome)
               if(self.max401kMatch>self.assets.g401k_currentContribution):
                  display.append(str(i)+": Increase your 401k contribution to $"+str(int(self.max401kMatch))+".")
                  i+=1
            elif (self.assets.g401k_employerMatch=="IDK"):
               display.append(str(i)+": Find out if your employer matches any portion of your 401k contribution.")
               i+=1
         elif (self.assets.g401k_have=="False"):
            display.append(str(i)+": Start your 401k and contribute up to "+self.max401kMatch+".")
            i+=1
         elif (self.assets.g401k_have=="IDK"):
            display.append(str(i)+": Find out if you already have a 401k or qualified for one.")
            i+=1
      elif (self.assets.g401k_employerOffer=="IDK"):
         display.append(str(i)+": Find out if your employer offers 401k.")
         i+=1
      

      #mid interest pay down
      for interest in self.liabilities.liabilities_interest:
         if ((float(interest)>=7) and (float(interest)<15)):
            display.append(str(i)+": "+"Pay off the loans with interest rate of 7 percent or higher.")
            i+=1
            break

      #HSA
      if (self.assets.HSA_haveHighDeductible=="True"):
         if(self.assets.HSA_haveHSA=="True"):
            #ASSUME single status and cap of $3300
            if(self.assets.HSA_contribution<3300):
               display.append(str(i)+": Increase your HSA contribution to $3300.")
               i+=1
         elif(self.assets.HSA_haveHSA=="IDK"):
            display.append(str(i)+": Create a HSA account and contribute up to $3300.")
            i+=1

      elif (self.assets.HSA_haveHighDeductible=="IDK"):
         display.append(str(i)+": Find out if you have a high deductible insurance plan so that you may qualify for a HSA account.")
         i+=1


      #low interest loans
      for interest in self.liabilities.liabilities_interest:
         if ((float(interest)>=4) and (float(interest)<7)):
            display.append(str(i)+": "+"Pay off the loans with interest rate of 4 percent or higher.")
            i+=1
            break


      #IRA
      if (self.assets.IRA_contribute=="True"):
         if(self.assets.IRA_contribution<5500):
            display.append(str(i)+": Increase your IRA contribution to $5500.")
            i+=1
            ##check if you are maxed out with ROTH
      elif (self.assets.IRA_contribute=="IDK"):
         display.append(str(i)+": Find out if you have been contributing to an IRA .")
         i+=1

      #super low interest loans
      for interest in self.liabilities.liabilities_interest:
         if ((float(interest)>=0) and (float(interest)<4)):
            display.append(str(i)+": "+"Pay off other low interest loans.")
            i+=1
            break

      #taxable investment
      #add some codes to tell how much money you can save

      self.displayContents+=display

   def displayResults(self):
      #i=0
      for line in self.displayContents:
         #if(i>0):
         #   line=str(i)+":"+line
         #i+=1
         print line



class Basic:
   def __init__(self,basicInfoArray):
      self.basicInfoArray=basicInfoArray
      self.basicInfo_monthyExpense=float(basicInfoArray[0])
      self.basicInfo_haveEmergencyFund=basicInfoArray[1]
      self.basicInfo_emergencyFund=float(basicInfoArray[2])
      self.basicInfo_grossIncome=float(basicInfoArray[3])


class Liability:
   def __init__(self,interestArray):
      self.interestArray=interestArray
      self.liabilities_interest=interestArray

class Asset:
   def __init__(self, g401kArray, HSAArray, IRAArray, taxableArray):
      self.g401kArray=g401kArray
      self.HSAArray=HSAArray
      self.IRAArray=IRAArray
      self.taxableArray=taxableArray

      self.g401k_employerOffer = g401kArray[0]
      self.g401k_have = g401kArray[1]
      self.g401k_employerMatch =g401kArray[2]
      self.g401k_matchPercent =float(g401kArray[3])
      self.g401k_uptoPercent =float(g401kArray[4])
      self.g401k_currentContribution =float(g401kArray[5])

      #HSA
      self.HSA_haveHighDeductible=HSAArray[0]
      self.HSA_haveHSA=HSAArray[1]
      self.HSA_contribution=float(HSAArray[2])
      self.HSA_SingleOrFamily=HSAArray[3]

      #IRA
      self.IRA_contribute=IRAArray[0]
      self.IRA_contribution=float(IRAArray[1])
      self.IRA_RothOrTraditional=IRAArray[2]

      #Taxable income
      self.taxable_have=taxableArray[0]

      self.taxable_contribution=float(taxableArray[1])

