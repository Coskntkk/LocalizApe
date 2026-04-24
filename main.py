import os
import json
import re
import requests
import shutil
from datetime import datetime
from dotenv import load_dotenv

# Load Configuration and Environment
load_dotenv()

def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: 'config.json' not found. Please create it based on the template.")
        exit(1)

config = load_config()
API_KEY = os.getenv("DEEPL_API_KEY")
LANG_FOLDER = config.get('project_path')
MASTER_FILE = config.get('master_file', 'enUS.json')
SHOULD_BACKUP = config.get('backup', True)

# API URL Selection
BASE_URL = "https://api-free.deepl.com/v2/translate" if API_KEY and API_KEY.endswith(":fx") else "https://api.deepl.com/v2/translate"

def create_backup(file_path):
    """Creates a timestamped backup of the target file."""
    if not SHOULD_BACKUP or not os.path.exists(file_path):
        return

    backup_dir = os.path.join(LANG_FOLDER, "backups")
    os.makedirs(backup_dir, exist_ok=True)
    
    file_name = os.path.basename(file_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"{timestamp}_{file_name}")
    
    shutil.copy2(file_path, backup_path)
    print(f"  [!] Backup created: {os.path.basename(backup_path)}")

def get_deepl_code(filename):
    """Normalizes filenames to DeepL compatible ISO codes."""
    clean_name = filename.replace(".json", "")
    match = re.match(r"([a-z]{2})[-_]?([a-z]{2})?", clean_name, re.I)
    
    if not match:
        return clean_name.upper()[:2]

    lang = match.group(1).upper()
    region = match.group(2).upper() if match.group(2) else ""

    if lang in ["EN", "PT"] and region:
        return f"{lang}-{region}"
    
    return "ZH" if lang == "ZH" else lang

def translate_batch(texts, target_lang_code):
    """Sends a batch of texts to DeepL API for translation."""
    if not texts:
        return []

    headers = {"Authorization": f"DeepL-Auth-Key {API_KEY}"}
    data = {
        "text": texts,
        "target_lang": target_lang_code,
        "context": "UI string for software/game interface status and controls.",
        "tag_handling": "xml"
    }
    
    try:
        r = requests.post(BASE_URL, headers=headers, data=data)
        r.raise_for_status()
        return [t["text"] for t in r.json()["translations"]]
    except Exception as e:
        print(f"  [X] Batch translation error: {str(e)}")
        return [f"TRANSLATION_ERROR: {str(e)}"] * len(texts)

def start_sync():
    master_path = os.path.join(LANG_FOLDER, MASTER_FILE)
    if not os.path.exists(master_path):
        print(f"Critical Error: Master file '{MASTER_FILE}' not found.")
        return

    with open(master_path, 'r', encoding='utf-8') as f:
        master_data = json.load(f)

    target_files = [f for f in os.listdir(LANG_FOLDER) if f.endswith('.json') and f != MASTER_FILE]
    
    if not target_files:
        print("No target language files found.")
        return

    for file_name in target_files:
        file_path = os.path.join(LANG_FOLDER, file_name)
        deepl_code = get_deepl_code(file_name)
        
        print(f"\n>>> Processing: {file_name} (ISO: {deepl_code})")
        create_backup(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                current_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            current_data = {}

        keys_to_translate = []
        texts_to_translate = []
        updated_data = {}

        # Identify what needs translation
        for key, value in master_data.items():
            if key in current_data and "TRANSLATION_ERROR" not in str(current_data[key]):
                updated_data[key] = current_data[key]
            else:
                keys_to_translate.append(key)
                texts_to_translate.append(value)

        # Execute batch translation
        if texts_to_translate:
            print(f"  [+] Translating {len(texts_to_translate)} new/missing keys...")
            translated_results = translate_batch(texts_to_translate, deepl_code)
            
            for key, translated_text in zip(keys_to_translate, translated_results):
                updated_data[key] = translated_text

        # Final reconstruction to match Master order
        ordered_data = {key: updated_data.get(key, "") for key in master_data.keys()}

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(ordered_data, f, indent=4, ensure_ascii=False)
        
        print(f"Done. Sync complete for {file_name}. Keys processed: {len(texts_to_translate)}")

if __name__ == "__main__":
    if not API_KEY:
        print("Error: DEEPL_API_KEY environment variable is missing.")
    else:
        print("""
        -------------------------------------------------------------
        LocalizApe v1.0
        [Localized Object Composition & Automated Lexicon Integration]
        -------------------------------------------------------------
        A WiseMonkeES Open Source Utility
        """)
        start_sync()
        print("\nAll files are synchronized.")