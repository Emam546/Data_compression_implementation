from __funct import *
import sys
import os
EXTENSION=".huf"
def compress(file_path):
	result_path=os.path.splittext(file_path)[0]+EXTENSION
	transferData_file(file_path,result_path)
def extract(file_path):
	result_path=os.path.splittext(file_path)[0]+'res'
	retransfer_file(file_path,)


if len(sys.argv)>1:
	try:
		if sys.argv[1]=="exctract":
			for file_path in sys.argv[2:]:
				extract(file_path)
		else:
			for file_path in sys.argv[1:]:
				compress(file_path)
		print("FILE WAS COMPRESSED")

	except Exception as e:
		print(e)
else:
	print("FILED NAME MUST EXIST")