import base64

def encode(image):
	#convert image to byte type
	with open(image, "rb") as image_file:
		encoded_string1 = base64.b64encode(image_file.read())

	#convert byte to string
	encoded_string = encoded_string1.decode("utf-8")
	return encoded_string

def decode(base64_string):
	decoded_data=base64.b64decode(base64_string)

	#write the decoded data back to original format in  file
	img_file = open('image.jpg', 'wb')
	img_file.write(decoded_data)
	img_file.close()