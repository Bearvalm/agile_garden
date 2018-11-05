import re


def name_is_not_correct(name):
	rule = '([^a-zA-Z0-9_])'
	parser = re.compile(rule, re.I | re.VERBOSE)
	result = parser.findall(name)
	return bool(result)