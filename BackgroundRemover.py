from rembg import remove
from PIL import Image
import io

input_path = 'image.jpg'
output_path = 'output_image.png'

# Dosyayı aç ve arka planı kaldır
with open(input_path, 'rb') as i:
    input_data = i.read()
    output_data = remove(input_data)

# Sonucu kaydet
with open(output_path, 'wb') as o:
    o.write(output_data)

print("İşlem tamamlandı!")