# coding: utf-8

import inspect
import sys


def get_current_function_name():
	return inspect.stack()[1][3]


class MyClass:
	def function_one(self):
		print "%s.%s invoked" % (self.__class__.__name__, get_current_function_name())


def atest():
	print sys._getframe().f_code.co_name
	b = sys._getframe()


if __name__ == "__main__":
	myclass = MyClass()
	myclass.function_one()
	atest()
