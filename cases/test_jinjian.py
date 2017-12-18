# coding:utf-8

from common.login import Login


class HH(Login):
	
	def __init__(self):
		Login.__init__(self, username='xn018170', env="SIT")
		
	def test(self):
		print(self.user_info)


if __name__ == '__main__':
	h1 = HH()
	print(h1.test())
	print h1.url
