import pyqrcode

url = input("enter url to generate to qr code: ")

qr_code = pyqrcode.create(url)
qr_code.svg('qrcode.svg',scale=5)
