# LocalizApe
*Localized Object Composition & Automated Lexicon Integration*

A professional synchronization utility designed to manage multi-language JSON localization files via the **DeepL API**.

---

## 🚀 Core Philosophy
This tool operates on a **"Master-Driven"** principle, treating your primary language file (e.g., `enUS.json`) as the single source of truth for your project's structure.

### Key Features
- **Structural Mirroring:** All target files are reconstructed to match the exact key order of the master file.
- **Per-Key Context:** Optional `context.json` supplies translation hints for each key via DeepL’s `context` parameter (never translated or synced as a locale file).
- **Batch Translation:** Keys that share the same context string are translated together in one API request.
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
        "context_file": "context.json",
        "backup": true
    }
```
`context_file` is optional and defaults to `context.json`.

### 4. Per-Key Context (context.json)
Place an optional `context.json` in the same folder as your language files (`project_path`). It uses the **same keys** as your master file; each value is a short hint describing what that string means in your UI (where it appears, what it does).

Example:
```json
    {
        "TITLE_MENU_PLAY": "Play button in the main menu. Starts game.",
        "PAUSE_PANEL_CONTINUE": "Return to the game button on the Pause Panel."
    }
```

**Behavior:**
- `context.json` is **read only** — it is never translated, overwritten, or treated as a target language file.
- When translating a key, LocalizApe passes the matching context value to DeepL. Keys missing from `context.json` use a built-in default UI/game context string.
- Keys with the same context text are batched into a single DeepL request; different contexts are sent in separate requests (order is preserved).

**Tips:** Keep hints concise and descriptive (screen, control type, meaning). DeepL uses `context` to disambiguate wording, not as a full prompt. If `context.json` is absent, behavior is unchanged from before — all keys use the default context.

## 💻 Usage
Simply run the script to synchronize all language files in your target folder:
```bash
    python main.py
```

### How it works:
1. **Scanning:** The script loads `master_file` and optional `context.json`, then finds all other `.json` files in `project_path` (master and context files are skipped).
2. **Comparison:** Each locale file is checked against the master to find missing keys or values containing `TRANSLATION_ERROR`.
3. **Translation:** New keys are sent to DeepL with per-key context from `context.json` when available; keys sharing the same context are batched together.
4. **Finalization:** Target files are updated so their keys and order match the master exactly.

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