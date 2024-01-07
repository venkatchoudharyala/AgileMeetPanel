from cryptography.fernet import Fernet
import base64
import datetime

def KeyGenerator():
	Key = Fernet.generate_key()
	#Key = base64.urlsafe_b64encode(Key).decode()
	return(Key.decode())

def MessageEncrypt(Message, Key):
	FernetObj = Fernet(Key.encode())

	#Key = base64.b64decode(Key)

	return((FernetObj.encrypt(Message.encode())).decode())

def MessageDecrypt(Message, Key):
	FernetObj = Fernet(Key.encode())

	#Key = base64.b64decode(Key)

	return(FernetObj.decrypt(Message.encode()).decode())

#print(type(Fernet.generate_key()))
#DriverCode
"""
Key = KeyGenerator()
Message = "Hi Im Blacky!"
print(f"Encrypted Message: {MessageEncrypt(Message, Key)}")
Message = MessageEncrypt(Message, Key)
print(f"Decrypted Message: {MessageDecrypt(Message, Key).decode()}")
"""
