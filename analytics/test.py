import qrcode

# Текст, который вы хотите закодировать в QR-коде
text_to_encode = "Пример текста для QR-кода"

# Создание объекта QRCode
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Добавление данных в объект QRCode
qr.add_data(text_to_encode)
qr.make(fit=True)

# Создание изображения QR-кода
qr_img = qr.make_image(fill_color="black", back_color="white")

# Сохранение изображения QR-кода
qr_img.save("qrcode.png")

print("QR-код успешно создан и сохранен в файле 'qrcode.png'")