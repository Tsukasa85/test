# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
#from wtforms import Form
from wtforms import Field, StringField, DecimalField, SubmitField, BooleanField, FormField, validators, IntegerField, TextField, RadioField, SelectField, HiddenField, ValidationError
from wtforms.validators import InputRequired, Required, StopValidation
from wtforms.fields import Label
from wtforms.widgets import TextInput

'''
class TagListField(Field):
    widget = TextInput()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []
'''
def check_positive_float(val):
	try:
		a = float(val)
	except ValueError:
		flag= False
	else:
		flag= True
		if (a<0):
			flag=False
	return flag

def validate_float(form,field):
	flag=check_positive_float(field.data)

	if (flag==False):
		raise ValidationError('You must enter a number greater than or equal to 0.')

class NameForm(Form):
    name = StringField('What is your name?', [Required()])
    submit = SubmitField('Submit')


class BasicInfoForm(Form):
	'''
	def validate_emergencyFund(form,field):
		if (form.haveEmergencyFund.data=='True'):
			validate_float(form,field)
			#validate_float(form,field)
'''
	groupName="Basic Information"
	monthlyExpense = StringField('What is your minimum monthly expenses?',validators=[Required(),validate_float], description="$")
	haveEmergencyFund = RadioField('Do you have an emergency fund?', validators=[Required()], choices=[("True","Yes"),("False","No"),("IDK","I don't know")])
	emergencyFund = StringField('How much do you have for your emergency fund?', description="$")
	grossIncome = StringField('What is your gross income?',validators=[Required(), validate_float], description = "$")
	submit = SubmitField('Next')
	
	def validate(self):
		rv = Form.validate(self)
		if not rv:
			return False

		if (self.haveEmergencyFund.data=='True'):
			if(not check_positive_float(self.emergencyFund.data)):
				self.emergencyFund.errors.append('The emergency fund must be a number greater than or equal to 0.')
				return False
		return True
	
	

class LiabilitiesForm(Form):
	groupName="Liabilities"
	#validationText=Label(field_id="validationText",text="hello")
	liabilities=HiddenField()
	submit = SubmitField('Next')

	def validate(self):
		rv = Form.validate(self)
		if not rv:
			return False
		rawData=[]
		if(self.liabilities.data!=""):
			rawData=self.liabilities.data.split(',')
			rawData.pop()
			for val in rawData:
				if (not check_positive_float(val)):
					self.liabilities.errors.append('The interest rate must be a number greater than or equal to 0.')
					return False

		return True


	#interestArray=StringField('Do you have an loans?  List out the interest rates separated by commas.', validators=[Required()], description = "%")




class AssetsForm(Form):
	def __init__(self, *args, **kwargs):
		kwargs['csrf_enabled'] = True
		super(AssetsForm, self).__init__(*args, **kwargs)
	groupName="Assets"
	g401k_employerOffer =RadioField('Does your employer offer 401k?',choices=[("True","Yes"),("False","No"),("IDK","I don't know")], default="True")
	g401k_have =RadioField('Do you have a 401k?',choices=[("True","Yes"),("False","No"),("IDK","I don't know")], default="True")
	g401k_employerMatch =RadioField('Does your employer match any portion of your 401k contribution?',choices=[("True","Yes"),("False","No"),("IDK","I don't know")], default="True")
	g401k_matchPercent =StringField('How much does your employer match?',validators=[Required()], default = 50 , description="%")
	g401k_uptoPercent =StringField('Up to how much does your employer match',validators=[Required()], default = 8, description = "%")
	g401k_currentContribution =StringField('How much do you contribute to 401k? (exclude company match up)',validators=[Required()], default = 1200, description="$")

	HSA_haveHighDeductible = RadioField('Do you have a high deductible insurance plan?',choices=[("True","Yes"),("False","No"),("IDK","I don't know")], default="True")
	HSA_haveHSA = RadioField('Do you have a HSA account?',choices=[("True","Yes"),("False","No"),("IDK","I don't know")], default="True")
	HSA_contribution = StringField('How much do you contribute to your HSA?',validators=[Required()], default = 3000, description ="$")
	HSA_SingleOrFamily = SelectField('Do you claim your taxes as Single or Family?',choices=[("Single","Single"),("Family","Family")], default = "Single")

	IRA_contribute=RadioField('Do you contribute to IRA?',choices=[("True","Yes"),("False","No"),("IDK","I don't know")], default="True")
	IRA_contribution=StringField('How much do you contribute to your IRA?',validators=[Required()], default = 5000, description ="$")
	IRA_RothOrTraditional=SelectField('Do you have Roth or Traditional IRA?',choices=[("IRA","IRA"),("Traditional","Traditional")], default = "Roth")

	taxable_have=RadioField('Do you have taxable investments (stocks, bonds, etc)?',choices=[("True","Yes"),("False","No"),("IDK","I don't know")], default="True")
	taxable_contribution=StringField('How much do you contribute towards your taxable investment accounts?',validators=[Required()], description ="$", default = 1200)

	submit = SubmitField('Next')
	

class FinanceForm(Form):
	BasicGroup = FormField(BasicInfoForm)

	LiabilitiesGroup = FormField(LiabilitiesForm)
	AssetsGroup = FormField(AssetsForm)	
	submit = SubmitField('Submit')

