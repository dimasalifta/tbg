from googletrans import Translator

# Teks dalam bahasa Mandarin
teks_mandarin = "\u4fe1\u53f7\u540d - \u82f1\u6587\u63cf\u8ff0 - \u4e2d\u6587\u63cf\u8ff0 - \u63a5\u53e3\u7c7b\u578b - \u503c\u7c7b\u578b - \u503c\u63cf\u8ff0 - \u5355\u4f4d - \u6743\u9650"

# Membuat objek translator
translator = Translator()

# Menerjemahkan teks dari bahasa Mandarin ke bahasa Inggris
terjemahan = translator.translate(teks_mandarin, src='zh-cn', dest='en')

print("Teks dalam Bahasa Mandarin:", teks_mandarin)
print("Terjemahan dalam Bahasa Inggris:", terjemahan.text)
