import glob
import os
import subprocess
import sys

def DownloadAndUnpack(id):
	"""
	Downloads and unpacks a paper
	Argument: Arxiv ID
	Returns: None
	"""
	idreplaced = str(id).replace('/', '') #for better handling of old arxiv IDs
	os.system('mkdir '+idreplaced) #tar command requires directory created
	command = 'wget arxiv.org/e-print/'+\
		str(id)+\
		' --output-document='+\
		idreplaced+\
		'downloaded'+\
		' --user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36" -P '+\
		str(id)
	os.system(command)
	filetype = subprocess.check_output("file "+idreplaced+'downloaded', shell=True)
	filetype = filetype.decode("utf-8") #convert bytes object returned by 'file' to string	
	#to parse the 'file' command output, we need position of filetype in the returned string
	pos = len(idreplaced+'downloaded')+2 #position of actual file type in the 'filetype string'	
	if (filetype[pos:pos+4]=='gzip'):
		command='tar -xvzf '+idreplaced+'downloaded -C '+idreplaced
		os.system(command)
	elif(filetype[pos:pos+3]=='PDF'):
		print('the paper was in PDF format, no uncompressing needed')
	elif(filetype[pos:pos+5]=='LaTeX'):
		print('the paper was in LaTeX format, no uncompressing needed')
	else:
		print('format not recognized, downloaded as is')

def PrintComments(id):
	"""
	Additional function to print comments (sometimes there is something authors did not want to show ; ) )
	Currently unused
	Argument: Arxiv ID
	Returns: None	
	"""
	for file in glob.glob(str(id)+"/*.tex"):
		print(file)
		with open(file,'r',encoding = "ISO-8859-1") as myfile:
			data=myfile.read()
		for ln in data.splitlines():	        
			if ln.startswith("%"):
		  		print(ln)

for arg in sys.argv[1:]:
	DownloadAndUnpack(arg)
