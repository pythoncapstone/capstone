import io, pdb, re
import PythonFileBuilder
import TestRunner
import FileParser
from capstone.PythonLib import PythonLib
from collections import namedtuple

#This class is called by the UserManager which interacts heavily with the front end
#It interacts with the File Parser component in order to achieve this
class UserCodeManager:
	USER_FILE_PATH = "UserFiles/"
	pythonFileBuilder = None
	userCodeFilePath = None
	stepNumber = None
	unitTests = None
	userCode = None
	userID = None
	userCodeException = None
	currentLineInUserCode = None

	def __init__(self, userID, userCode, unitTests):
		self.stepNumber = 0
		self.userID = userID
		self.userCode = userCode
		self.unitTests = unitTests
		self.pythonFileBuilder = PythonFileBuilder.PythonFileBuilder()
		self.userCodeFilePath =	self.pythonFileBuilder.buildFile(userCode + '\n' + unitTests, userID)
	
	#takes one step in the user code, runs the code, and then returns the result
	def executeStepInUserCode(self):
		self.stepNumber = self.stepNumber + 1
		self.__runFile()
		return self.__resultOfStepInUserCode()

	#executes through the entirity of the user's code
	def executeEntireUserCode(self):
		self.stepNumber = self.stepNumber + 1
		self.__runFile()
		while self.__resultOfStepInUserCode()['exception'] != 'End of File': #runs until end of code
			self.stepNumber += 1
			self.__runFile()
			if self.__resultOfStepInUserCode()['exception'] == 'End of File':
				self.stepNumber -= 1
				self.__runFile()
				return self.__resultOfStepInUserCode()

	def runTestsOnUserCode(self):
		testRunner = TestRunner.TestRunner(self.userID, self.userCode, self.unitTests)
		return testRunner.getResults()

	#returns line number
	def __lineCount(self):
		lineCount = 0
		for character in self.userCode:
			if character == '\n':
				lineCount += 1
		return lineCount + 1

	#runs through the output from the debugger from the File Parser
	#and writes the information in a readable manner to a result file
	def __runFile(self):
		PythonLib.ensureDirectoryExists(self.USER_FILE_PATH)
		outputFromDebugger = open(self.USER_FILE_PATH + self.userID + 'ResultFile.txt', 'w+')
		inputForDebugger = io.StringIO(unicode(self.pythonFileBuilder.getPdcInstructions(self.stepNumber)))
		#print str(self.pythonFileBuilder.getPdcInstructions(self.stepNumber))
		debugger = pdb.Pdb(completekey='tab', stdin=inputForDebugger, stdout=outputFromDebugger)
		self.userCodeException = ''

		#generate the result file
		try:
			debugger.run('import ' + self.userCodeFilePath, {}, {})
			fileParser = FileParser.FileParser(self.USER_FILE_PATH + self.userID + 'ResultFile.txt')
			self.currentLineInUserCode = fileParser.get_current_line()
			#print '\n \n TEST: ' , fileParser.wrapper_Function_Counter , '\n \n'

		#if there was an exception, we print that out instead
		except Exception, e:
			print "\n\n__runFile = " + str(e) + "\n\n"
			self.userCodeException = PythonLib.parseExceptionMessage(e)
			# Exception line number is off by eight
			self.currentLineInUserCode = PythonLib.parseExceptionLineNumber(e)-8

		finally:
			outputFromDebugger.close()
			inputForDebugger.close()

	#creates an object that contains information about
	#line number, local vars, and stack information about the frame
	#will also return information about the exception if applicable
	def __resultOfStepInUserCode(self):
		fileParser = FileParser.FileParser(self.USER_FILE_PATH + self.userID + 'ResultFile.txt')
		userStepResult = {}

		if (fileParser.wrapper_Function_Counter == 0 and self.userCodeException == ''): #this means we've hit the end of file
			userStepResult['exception'] = 'End of File'
		else:
			userStepResult['exception'] = self.userCodeException
			userStepResult['lineNumber'] = self.currentLineInUserCode
			userStepResult['localVars'] = fileParser.get_local_vars()
			userStepResult['stackInfo'] = fileParser.get_functions_including_vars()

		return userStepResult