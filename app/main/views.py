from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm, FinanceForm
from classes import *


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))

@main.route('/calc', methods=['GET', 'POST'])
def calc():
    form = FinanceForm()
    if form.validate_on_submit():
        #this portion of the code is for when the submission has been made.
        returnList=[form.monthlyExpense.data]
        returnList.append(form.enable401k.data)
        returnList.append(form.matchup401k.data)
        returnList.append(form.emergencyFund.data)
        returnList.append(form.loanInterest.data)


        session['Basic']=returnList
        
        return redirect(url_for('.result'))
        
    return render_template('calc.html',form=form) #this is universal rendering of the page

@main.route('/result', methods=['GET'])
def result():
    #Run the logic then render
    basic=Basic(session.get('Basic')[0], session.get('Basic')[1], session.get('Basic')[2])
    liabilities=[Liability(session.get('Basic')[4])]
    assets=[Asset(session.get('Basic')[3])]
    model=Model(basic,liabilities,assets)
    model.run()
    return render_template('result.html',datas=model.display)
