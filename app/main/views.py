from flask import render_template, session, redirect, url_for, current_app, request
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm, FinanceForm, BasicInfoForm, LiabilitiesForm, AssetsForm
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
        basicForm=form.BasicGroup
        #this portion of the code is for when the submission has been made.
        BasicInfoList=[basicForm.monthlyExpense.data]
        BasicInfoList.append(basicForm.haveEmergencyFund.data)
        BasicInfoList.append(basicForm.emergencyFund.data)
        BasicInfoList.append(basicForm.grossIncome.data)
        session['BasicInfo']=BasicInfoList

        session['Liabilities']=form.LiabilitiesGroup.interestArray.data

        assetForm=form.AssetsGroup
        g401kArray=[assetForm.g401k_employerOffer.data]
        g401kArray.append(assetForm.g401k_have.data)
        g401kArray.append(assetForm.g401k_employerMatch.data)
        g401kArray.append(assetForm.g401k_matchPercent.data)
        g401kArray.append(assetForm.g401k_uptoPercent.data)
        g401kArray.append(assetForm.g401k_currentContribution.data)
        session['g401kArray']=g401kArray

        HSAArray=[assetForm.HSA_haveHighDeductible.data]
        HSAArray.append(assetForm.HSA_haveHSA.data)
        HSAArray.append(assetForm.HSA_contribution.data)
        HSAArray.append(assetForm.HSA_SingleOrFamily.data)
        session['HSAArray']=HSAArray

        IRAArray=[assetForm.IRA_contribute.data]
        IRAArray.append(assetForm.IRA_contribution.data)
        IRAArray.append(assetForm.IRA_RothOrTraditional.data)
        session['IRAArray']=IRAArray

        taxableArray=[assetForm.taxable_have.data]
        taxableArray.append(assetForm.taxable_contribution.data)
        session['taxableArray']=taxableArray
        
        return redirect(url_for('.result'))
    return render_template('calc.html',form=form) #this is universal rendering of the page

@main.route('/basicinfo', methods=['GET', 'POST'])
def basicinfo():
    form = BasicInfoForm()
    sesh=[]
    if form.validate_on_submit():
        #this portion of the code is for when the submission has been made.
        BasicInfoList=[form.monthlyExpense.data]
        BasicInfoList.append(form.haveEmergencyFund.data)
        BasicInfoList.append(form.emergencyFund.data)
        BasicInfoList.append(form.grossIncome.data)
        session['BasicInfo']=BasicInfoList
        sesh=session['BasicInfo']
        
        return redirect(url_for('.liabilities'))
    return render_template('basicinfo.html',form=form, sesh=sesh) #this is universal rendering of the page

@main.route('/liabilities', methods=['GET', 'POST'])
def liabilities():
    form = LiabilitiesForm()
    sesh=[]
    if form.validate_on_submit():
        rawData=[]
        if(form.liabilities.data!=""):
            rawData=form.liabilities.data.split(',')
            rawData.pop()
        session['Liabilities']=rawData
        sesh=session['Liabilities']
        
        return redirect(url_for('.assets'))
    return render_template('liabilities.html',form=form,sesh=sesh) #this is universal rendering of the page

@main.route('/assets', methods=['GET', 'POST'])
def assets():
    form = AssetsForm()
    if form.validate_on_submit():
        g401kArray=[form.g401k_employerOffer.data]
        g401kArray.append(form.g401k_have.data)
        g401kArray.append(form.g401k_employerMatch.data)
        g401kArray.append(form.g401k_matchPercent.data)
        g401kArray.append(form.g401k_uptoPercent.data)
        g401kArray.append(form.g401k_currentContribution.data)
        session['g401kArray']=g401kArray

        HSAArray=[form.HSA_haveHighDeductible.data]
        HSAArray.append(form.HSA_haveHSA.data)
        HSAArray.append(form.HSA_contribution.data)
        HSAArray.append(form.HSA_SingleOrFamily.data)
        session['HSAArray']=HSAArray

        IRAArray=[form.IRA_contribute.data]
        IRAArray.append(form.IRA_contribution.data)
        IRAArray.append(form.IRA_RothOrTraditional.data)
        session['IRAArray']=IRAArray

        taxableArray=[form.taxable_have.data]
        taxableArray.append(form.taxable_contribution.data)
        session['taxableArray']=taxableArray

        return redirect(url_for('.results'))
    return render_template('assets.html',form=form) #this is universal rendering of the page

@main.route('/results', methods=['GET'])
def results():
    #Run the logic then render
    basic=Basic(session.get('BasicInfo'))
    liabilities=Liability(session.get('Liabilities'))
    assets=Asset(session.get('g401kArray'), session.get('HSAArray'), session.get('IRAArray'), session.get('taxableArray'))
    model=Model(basic,liabilities,assets)
    model.createInputSummary()
    model.run()
    return render_template('result.html',inputSummary=model.inputSummary, datas=model.displayContents)
