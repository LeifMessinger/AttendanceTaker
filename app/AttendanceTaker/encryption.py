#Takes a binary string, returns a binary string, which means you probably gotta .encode() it
def encryptAtTime(binaryString):
	from django.conf import settings
	from cryptography.fernet import Fernet
	fernet = Fernet(settings.FERNET_KEY)

	import time
	urlSafeB64String = fernet.encrypt_at_time(binaryString, int(time.time()))

	return encryptedString

#Takes a binary string, returns a binary string, which means you probably gotta .encode() it
#Returns None if it is a bad key
def decryptAtTime(binaryString, numSecondsGood=1000000):
	from django.conf import settings
	from cryptography.fernet import Fernet
	fernet = Fernet(settings.FERNET_KEY)

	import time
	import cryptography
	try:
		return fernet.decrypt_at_time(binaryString, numSecondsGood, int(time.time()))
	except cryptography.fernet.InvalidToken:
		return None

RECIEPT_SALT = b"reciept" #Don't ever change this. If you do, it'll nullify all of the reciepts out there.

#os.urandom(16) if you want a random salt
#Redefined in AttendanceTaker/views.py
def makeFernetKey(salt):
	import base64
	import os
	from django.conf import settings	#For the SECRET_KEY
	from cryptography.fernet import Fernet
	from cryptography.hazmat.primitives import hashes
	from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
	password = settings.SECRET_KEY.encode()
	kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt,
		iterations=480000,
	)
	return base64.urlsafe_b64encode(kdf.derive(password))

def serverEncrypt(string, seed = b""):
	from django.conf import settings
	from cryptography.fernet import Fernet
	fernet = Fernet(makeFernetKey(seed))

	return fernet.encrypt(string)

def serverDecrypt(string, seed = b""):
	from django.conf import settings
	from cryptography.fernet import Fernet
	fernet = Fernet(makeFernetKey(seed))

	import cryptography
	try:
		return fernet.decrypt(string)
	except cryptography.fernet.InvalidToken:
		return None
