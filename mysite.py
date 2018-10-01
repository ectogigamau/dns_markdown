from ftplib import FTP

HOST = 'ftp.blabla.com'
USER = 'UserName'
PASSWORD = 'Password'

SITE_DIR = 'htdocs'

def update(filenames):
	print('connect to site..')
	ftp = FTP(HOST)
	try:
		ftp.login(USER, PASSWORD)
		ftp.cwd(SITE_DIR)	

		print('update site..')
		for filename in filenames:
			print('  update ' + filename + '..')
			f = open(filename, "r")
			send = ftp.storbinary('STOR ' + filename, f)

		ftp.quit()
		print('site is updated!')
	except:
		print('site is NOT updated!')
	#	pass