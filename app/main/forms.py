# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, DecimalField, SubmitField, BooleanField
from wtforms.validators import Required

def isfloat(x):
	try:
		a = float(x)
	except ValueError:
		return False
	else:
		return True

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class FinanceForm(Form):
	monthlyExpense = StringField('What is your minimum monthly expenses?',validators=[Required()])
	enable401k = BooleanField('Does your employer offer 401k?')
	matchup401k = StringField('Up to what percentage does the employer match your 401k contribution?',validators=[Required()])
	emergencyFund = StringField('How much do you have for your emergencyFund?',validators=[Required()])
	loanInterest = StringField('What is the interest rate on your loan?',validators=[Required()])
	
	submit = SubmitField('Submit')

	def validate(self):
		rv = Form.validate(self)
		if not rv:
			return False


		if not isfloat(self.monthlyExpense.data):
			self.monthlyExpense.errors.append('It must be a positive number.')
			return False
		else:
			if float(self.monthlyExpense.data) < 0:
				self.monthlyExpense.errors.append('It must be a positive number.')
				return False

		return True


