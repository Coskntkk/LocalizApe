# LocalizApe
*Localized Object Composition & Automated Lexicon Integration*

A professional synchronization utility designed to manage multi-language JSON localization files via the **DeepL API**.

---

## 🚀 Core Philosophy
This tool operates on a **"Master-Driven"** principle, treating your primary language file (e.g., `enUS.json`) as the single source of truth for your project's structure.

### Key Features
- **Structural Mirroring:** All target files are reconstructed to match the exact key order of the master file.
- **Batch Translation:** Translates multiple keys in a single API request for maximum speed and efficiency.
- **Safety First:** Automatically creates timestamped backups in the `backups/` folder before any modification.
- **Smart Diffing:** Only translates missing keys or those marked with errors, preserving existing translations to save your DeepL quota.

---

## 🛠 Setup & Requirements

### 1. Prerequisites
- **Python 3.8+**
- Install dependencies:
```bash
    pip install requests python-dotenv
```

### 2. Private Configuration (.env)
Create a `.env` file in the root directory with the following content:
```env
DEEPL_API_KEY=your_deepl_api_key_here
```
Replace `your_deepl_api_key_here` with your actual DeepL API key.

### 3. Tool Configuration (config.json)
Set your project paths and preferences:
```json
    {
        "project_path": "/Absolute/Path/To/Your/Project/Languages",
        "master_file": "enUS.json",
        "backup": true
    }
```

## 💻 Usage
Simply run the script to synchronize all language files in your target folder:
```bash
    python main.py
```

### How it works:
1. Scanning: The script identifies all .json files within your project_path.
2. Comparison: It checks each file against the master_file to detect missing or errored keys.
3. Translation: New keys are grouped and sent to DeepL in efficient batches.
4. Finalization: Target files are updated, ensuring their structure and key order perfectly match the Master.

## ⚠️ Maintenance
Encoding: Always ensure your JSON files are saved in UTF-8 format.
Version Control: While the tool creates local backups, using Git is highly recommended for project safety.
API Limits: Monitor your character usage on the DeepL Dashboard.

## 🤝 Contributing & Feedback
Have a suggestion or found a bug? Your input is welcome!
- **Open an Issue:** If you encounter any bugs, please report them via the GitHub Issues tab.
- **Pull Requests:** Feel free to fork the repository and submit a PR with your improvements.
- **Feature Requests:** Suggest new features (like supporting other APIs or file formats) in the discussions.

---

## ⭐ Support the Project
If this tool saved you hours of localization work, consider giving it a **Star** ⭐️ on GitHub! It helps other developers find this project and keeps the motivation high for future updates.

*Developed with passion for game developers and software engineers.*