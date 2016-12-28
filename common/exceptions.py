class SkipTestException(Exception):
	def __init__(self, error):
		Exception.__init__(self)
		self.error = error