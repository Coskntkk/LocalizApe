import os
import json

def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: 'config.json' not found. Please create it based on the template.")
        exit(1)

config = load_config()
LANG_FOLDER = config.get('project_path')

def merge_align_and_clean(dict1, dict2):
    """
    dict1'i (1. dosya) mutlak şablon kabul eder:
    - Sadece dict1'de olan anahtarları korur (dict2'de olup dict1'de olmayanları siler).
    - dict1'in sıralamasını birebir uygular.
    - dict2'de olmayan yeni anahtarları boş string ("") olarak ekler.
    """
    aligned_dict = {}
    
    # Sadece dict1'deki (referans) anahtarlar üzerinden ilerliyoruz
    for key, val1 in dict1.items():
        if key in dict2:
            val2 = dict2[key]
            # Eğer her iki tarafta da değer bir sözlükse (iç içe JSON), rekürsif olarak içeri gir
            if isinstance(val1, dict) and isinstance(val2, dict):
                aligned_dict[key] = merge_align_and_clean(val1, val2)
            else:
                # 2. dosyada zaten varsa mevcut değerini koru
                aligned_dict[key] = val2
        else:
            # 1. dosyada var ama 2. dosyada yoksa:
            if isinstance(val1, dict):
                # Eğer eklenen değer bir alt sözlükse, onun da içini boşaltarak şablonunu oluştur
                aligned_dict[key] = merge_align_and_clean(val1, {})
            else:
                # Normal bir değerse boş string atayarak ekle
                aligned_dict[key] = ""
            
    return aligned_dict

def process_selected_json_files(folder_path, file1_name, file2_name):
    """
    Belirtilen klasördeki JSON dosyalarını işler ve 2. dosyayı günceller.
    """
    file1_path = os.path.join(folder_path, file1_name)
    file2_path = os.path.join(folder_path, file2_name)
    
    if not os.path.exists(file1_path) or not os.path.exists(file2_path):
        print("Hata: Belirtilen dosyalar klasörde bulunamadı.")
        return

    try:
        with open(file1_path, 'r', encoding='utf-8') as f1:
            data1 = json.load(f1)
        with open(file2_path, 'r', encoding='utf-8') as f2:
            data2 = json.load(f2)
    except json.JSONDecodeError as e:
        print(f"JSON okuma hatası: {e}")
        return

    # Eşitleme ve temizlik işlemini başlat
    updated_data2 = merge_align_and_clean(data1, data2)
    
    # Güncellenmiş veriyi Dosya 2'ye yaz
    with open(file2_path, 'w', encoding='utf-8') as f2_out:
        json.dump(updated_data2, f2_out, ensure_ascii=False, indent=4)
        
    print(f"Başarılı: '{file2_name}' dosyası güncellendi!")
# --- KULLANIM ÖRNEĞİ ---
# Klasör yolunu ve dosya isimlerini buraya yazabilirsin:
referans_dosya = "enUS.json"    # Eksik key'lerin alınacağı ve sıralamanın kopyalanacağı dosya (1.)
guncellenecek_dosya = "context.json" # Değerlerin korunacağı ama eksiklerin tamamlanacağı dosya (2.)

# Fonksiyonu çalıştır
process_selected_json_files(LANG_FOLDER, referans_dosya, guncellenecek_dosya)