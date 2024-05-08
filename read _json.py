import json

# Buka file JSON
with open('mc2600_oid_list.json') as f:
    data = json.load(f)

# Inisialisasi list untuk menyimpan objek JSON
json_list = []

# Tambahkan setiap objek JSON ke dalam list
for obj in data:
    json_list.append(obj)

# Sekarang json_list berisi semua objek JSON dalam file
print(json_list)
