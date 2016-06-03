import Image

buf = open('03_tmp.txt')

img = Image.new('RGB', (256,256))

for i in range(0,256):
	for j in range(0,256):
		c = buf.read(1)
		if c == '0':
			img.putpixel((i,j), 0xFFFFFFFF )
		else:
			img.putpixel((i,j), 0 )

img.save('test2.jpg')