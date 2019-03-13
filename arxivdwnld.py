import glob,os,re,subprocess, sys

#takes an Arxiv ID as argument, downloads and unpacks the corresponding paper
def DownloadAndUnpack(id):
	print('opening directory for paper '+str(id))
	idreplaced=str(id).replace('/', '') #for better handling of old arxiv IDs
	os.system('mkdir '+idreplaced)
	os.system('wget arxiv.org/e-print/'+str(id)+' --output-document='+idreplaced+'downloaded'+
				' --user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36" -P '
				+str(id))
	filetype = subprocess.check_output("file "+idreplaced+'downloaded', shell=True)
	filetype = filetype.decode("utf-8") #convert bytes object to string
	print('filetype retrieved: \n',filetype)	
	#to parse the 'file' command output, we need position of filetype in the returned string
	pos=len(idreplaced+'downloaded')+2
	print('filetype in position', filetype[pos:pos+4])	
	if (filetype[pos:pos+4]=='gzip'):
		print('uncompressing') 
		command='tar -xvzf '+idreplaced+'downloaded -C '+idreplaced
		print('command',command)
		os.system(command)
	elif(filetype[pos:pos+3]=='PDF'):
		print('the paper was in PDF format, no uncompressing needed')
	else:
		print('format not recognized, downloaded as is')

#additional function to print comments (sometimes there is something authors did not want to show ; ) )
#currently unused
def PrintComments(id):
	for file in glob.glob(str(id)+"/*.tex"):
		print(file)
		with open(file,'r',encoding = "ISO-8859-1") as myfile:
			data=myfile.read()
		for ln in data.splitlines():	        
			if ln.startswith("%"):
		  		print(ln)


for arg in sys.argv[1:]:
	DownloadAndUnpack(arg)
