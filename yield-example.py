def hello():
	for i in range(1000):
		yield i

while True:
	print(hello())