import json
from django.utils import simplejson
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, RequestContext, loader
from capstone.UserCode import UserManager

userManager = UserManager.UserManager()

#Views.py is called by urls.py
#Views.py will actually call the python code and return the result as a JSON object
#to see what each function does specifically, view their documentation in the appropriate python file

def index(request):
	return render_to_response('index.html', context_instance=RequestContext(request))

#calls startDebugging in UserManager.py
def startDebugging(request):
	try:
		userCode = request.GET['pythonCode']
		unitTests = request.GET['unitTests']
		request.session.save() 
		sessionIdForAnonymousUser = 'AnonymousUserSession' + request.session.session_key
		userManager.createUserCodeManager(sessionIdForAnonymousUser, userCode, unitTests);
		stepResult = userManager.executeStepInUserCode(sessionIdForAnonymousUser)
		testResults = userManager.runTestsOnUserCode(sessionIdForAnonymousUser);
		stepResult['testResults'] = testResults
		return HttpResponse(json.dumps(stepResult), mimetype="application/json")
	except Exception, e:
		print "\n\nstartDebugging exception = " + str(e) + "\n\n"

#calls takeStep in UserManager.py
def takeStep(request):
	sessionIdForAnonymousUser = 'AnonymousUserSession' + request.session.session_key
	stepResult = userManager.executeStepInUserCode(sessionIdForAnonymousUser)
	return HttpResponse(json.dumps(stepResult), mimetype="application/json")	

#calls runAll in UserManager.py
def runAll(request):
	userCode = request.GET['pythonCode']
	unitTests = request.GET['unitTests']
	request.session.save() 
	sessionIdForAnonymousUser = 'AnonymousUserSession' + request.session.session_key
	userManager.createUserCodeManager(sessionIdForAnonymousUser, userCode, unitTests);
	stepResult = userManager.executeEntireUserCode(sessionIdForAnonymousUser)
	testResults = userManager.runTestsOnUserCode(sessionIdForAnonymousUser);
	stepResult['testResults'] = testResults
	return HttpResponse(json.dumps(stepResult), mimetype="application/json")