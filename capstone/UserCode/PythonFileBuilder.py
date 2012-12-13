#This class creates a file for the user
#And inserts their code into it
#It also encapsulates the code with a wrapper that allows
#the class to get information about the current frame
#of the user's code
class PythonFileBuilder:
	STEPS_NEED_TO_FIRST_LINE = 6

	#builds the file with the user code
	#adds indents to lines where needed and wraps the code in a "Wrapper Function" to mantain status of locals
	def buildFile(self, code, filePrefix):
		code = self.__addTabToNewLines(code)
		code = self.__addWrapperFunction(code)
		code = self.__addFrameGetter(code)
		code = self.__addCallForWrapperFunction(code)
		newFilePath = self.__createUserCodeFile(code, filePrefix)
		return newFilePath

	#gets instructions from the debugger
	def getPdcInstructions(self, stepNumber):
		instructions = "step;;" * (stepNumber + self.STEPS_NEED_TO_FIRST_LINE)
		instructions = instructions + "getFramesAndVars();;list"
		return instructions

	#adds tabs to user code before including wrapper function
	def __addTabToNewLines(self, code):
		return code.replace('\n', '\n\t')

	#adds the wrapper function to the users code. this allows the frame to track locals in the debugger
	def __addWrapperFunction(self, code):
		return '\ndef WrapperFunction():\n\t' + code

	#this will be added at the end of the user's code
	def __addCallForWrapperFunction(self, code):
		return code + "\nWrapperFunction()"

	#accesses data about the current frame of the users code
	#the two main parts of this being f_code.co_name and f_locals
	#documentation for these frame member functions can be found at
	#the following url: http://docs.python.org/2/library/inspect.html
	def __addFrameGetter(self, code):
		frameGetter = 'import sys, inspect, linecache'
		frameGetter += '\ndef getFramesAndVars():'
		frameGetter += '\n\tbase = sys._getframe(0)'
		frameGetter += '\n\tf = base.f_back'
		frameGetter += '\n\twhile f.f_back:'
		frameGetter += '\n\t\tprint "FunctionName===" + str(f.f_code.co_name) + "===LocalVars: " + str(f.f_locals)'
		frameGetter += '\n\t\tf = f.f_back'
		return frameGetter + code

	#creates the code file for the specified user
	def __createUserCodeFile(self, code, filePrefix):
		fullFilePath = filePrefix + 'CodeFile.py'
		try:
			codeFile = open(fullFilePath, 'w+')
			codeFile.write(code)
		finally:
			codeFile.close()
		return fullFilePath