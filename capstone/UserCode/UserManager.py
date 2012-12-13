from capstone.UserCode import UserCodeManager

#Communicates with the front end
#Makes calls in UserCodeManager based on what was called from the front end
#The calls to this from the front end can be found in the "student\views.py"
class UserManager:
	userCodeManagers = None;

	def __init__(self):
		self.userCodeManagers = {}

	def createUserCodeManager(self, user, userCode, unitTests):
			self.userCodeManagers[user] = UserCodeManager.UserCodeManager(user, userCode, unitTests)

	def executeStepInUserCode(self, user):
		return self.userCodeManagers[user].executeStepInUserCode()

	def executeEntireUserCode(self, user):
		return self.userCodeManagers[user].executeEntireUserCode()

	def runTestsOnUserCode(self, user):
		return self.userCodeManagers[user].runTestsOnUserCode()