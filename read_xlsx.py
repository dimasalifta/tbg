import pandas as pd
import json

def convert_to_json(file_path):
    # Membaca file Excel
    df = pd.read_excel(file_path)
    
    # Mengubah kolom header menjadi lowercase
    df.columns = map(str.lower, df.columns)
    
    # Mengganti nilai NaN dengan string kosong
    df = df.fillna('')
    # Mengonversi DataFrame ke JSON
    json_data = df.to_dict(orient='records')
    
    return json_data

def main():
    file_path = 'MC2600 OID list V9.02150204.xlsx'  # Ganti dengan path file Excel yang sesuai
    json_data = convert_to_json(file_path)
    
    # Menyimpan data JSON ke file
    with open('data.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

if __name__ == "__main__":
    main()
