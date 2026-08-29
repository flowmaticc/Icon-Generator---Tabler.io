# 🎨 Icon Generator — Tabler Icons Manager

**Generador y gestor de iconos de Tabler Icons con previsualización en tiempo real**

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

---

<details>
<summary>🌍 <b>Missing your language?</b></summary>

### Want the app in Italian, Portuguese, or Klingon? 

You could open an *Issue* asking nicely, buuuut... we are in the AI era. You can do it yourself in less time than it takes to brew a coffee! ☕

**How to hack the system (Quick Guide):**

1. Copy all the content from the `language/gb.json` file (or the Spanish one, `es.json`).
2. Go to your trusty AI (ChatGPT, Gemini, Claude...).
3. Paste this magic *prompt*:
   > *"You are a professional translator. Translate the following UI JSON file of my app to **[INSERT YOUR LANGUAGE HERE]**. It is strictly important that you keep the keys intact and only translate the values. Do not give me any explanations, just return the clean JSON. Here it is: [PASTE JSON HERE]"*
4. Copy the AI's response.
5. Create a new file in the `language/` folder with your language code (e.g., `it.json` for Italian, `pt.json` for Portuguese) and paste the code inside.
6. **Done!** Open the program and your language will magically appear in the menu. ✨

*(P.S: If you've made a cool translation, make a Pull Request and we'll add it officially for everyone! 😉)*

</details>

---

<details>
<summary><h2>🇬🇧 English (Inglés)</h2></summary>

### 🎯 What is this?

A desktop tool in Python that allows you to **download, preview, and generate Tabler Icons** in multiple sizes, colors, and stroke widths.

Perfect for **designers, developers, and anyone** who needs icons for their personal or professional projects.

---

### ✨ Key Features

- 🎨 **Real-time preview** — Adjust size, color, and stroke and see the result instantly.
- 📥 **Automatic SVG download** — Fetches icons directly from the Tabler Icons CDN.
- 🖼️ **Bulk PNG generation** — Create hundreds of icons with all the combinations you need.
- 📂 **Automatic organization** — Saves PNGs in subfolders by size and stroke.
- 🎯 **Persistent selection** — Remembers which icons you selected between sessions.
- 🌍 **Multi-language** — Support for 6 languages.
- 🖱️ **Intuitive interface** — Dark, clean, and professional design.
- 🆓 **Completely free** — Open source, free for personal and commercial use.

---

### 🌍 Supported Languages

| Code | Language | File |
| :---: | :--- | :--- |
| 🇪🇸 `es` | Spanish | `es.json` |
| 🇬🇧 `gb` | English | `gb.json` |
| 🇩🇪 `de` | German | `de.json` |
| 🇫🇷 `fr` | French | `fr.json` |
| 🇯🇵 `jp` | Japanese | `jp.json` |
| 🇷🇺 `ru` | Russian | `ru.json` |

> **You can add more languages!** Just create a JSON file in the `language/` folder.

---

### 🖥️ Screenshots

<img width="1388" height="847" alt="image" src="https://github.com/user-attachments/assets/cea503f4-109a-4a3b-93e2-d1be3ef73f42" />

<p align="center">
  <img src="./media/2026-08-29%20150559.gif" alt="Icon Generator Demo" width="900">
</p>

<p align="center">
  <img src="./media/2026-08-29 151129.gif" alt="Icon Generator Demo" width="900">
</p>

---

### 🛠️ System Requirements

- **Python 3.8 or higher**
- **Cairo / GTK3 Runtime** (for SVG → PNG conversion)

---

### 📦 Dependency Installation

#### 1. Install Python

Download and install Python from [python.org](https://python.org/downloads/).

#### 2. Install Cairo (Required)

<details>
<summary><b>Windows</b></summary>

1. Download the **GTK3 Runtime** installer from [GTK for Windows Runtime Environment Releases](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases).
2. Run the installer and follow the instructions.
3. Restart your terminal.
</details>

<details>
<summary><b>Linux (Ubuntu/Debian)</b></summary>

```bash
sudo apt-get update
sudo apt-get install libcairo2-dev libgirepository1.0-dev
```
</details>

<details>
<summary><b>Linux (Fedora)</b></summary>

```bash
sudo dnf install cairo-devel
```
</details>

<details>
<summary><b>Linux (Arch)</b></summary>

```bash
sudo pacman -S cairo
```
</details>

<details>
<summary><b>macOS</b></summary>

```bash
# With Homebrew
brew install cairo

# With MacPorts
sudo port install cairo
```
</details>

#### 3. Install Python Dependencies

📄 **requirements.txt**

```text
Pillow>=10.0.0
requests>=2.31.0
cairosvg>=2.7.0
```

Run:

```bash
pip install -r requirements.txt
```

---

### 🚀 Installation and Execution

```bash
# 1. Clone the repository
git clone [https://github.com/your-username/icon-generator.git](https://github.com/your-username/icon-generator.git)
cd icon-generator

# 2. Create folders
mkdir icons
mkdir language

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the program
python icon_generator.py
```

---

### 🙏 Acknowledgments

- [Tabler Icons](https://tabler.io/icons) — For their incredible open source icon library.
- [CairoSVG](https://cairosvg.org/) — For the SVG to PNG conversion.

</details>

<details>
<summary><h2>🇩🇪 Deutsch (Alemán)</h2></summary>

### 🎯 Was ist das?

Ein Desktop-Tool in Python, mit dem Sie **Tabler-Icons herunterladen, in der Vorschau anzeigen und generieren** können – in verschiedenen Größen, Farben und Strichstärken (Stroke).

Perfekt für **Designer, Entwickler und jeden**, der Icons für persönliche oder berufliche Projekte benötigt.

---

### ✨ Hauptmerkmale

- 🎨 **Echtzeit-Vorschau** — Passen Sie Größe, Farbe und Stroke an und sehen Sie das Ergebnis sofort.
- 📥 **Automatischer SVG-Download** — Lädt Icons direkt vom Tabler Icons CDN herunter.
- 🖼️ **Massen-PNG-Generierung** — Erstellen Sie Hunderte von Icons mit allen gewünschten Kombinationen.
- 📂 **Automatische Organisation** — Speichert PNGs in Unterordnern nach Größe und Stroke.
- 🎯 **Persistente Auswahl** — Merkt sich Ihre ausgewählten Icons zwischen den Sitzungen.
- 🌍 **Mehrsprachigkeit** — Unterstützung für 6 Sprachen.
- 🖱️ **Intuitive Benutzeroberfläche** — Dunkles, sauberes und professionelles Design.
- 🆓 **Komplett kostenlos** — Open Source, frei für private und kommerzielle Nutzung.

---

### 🖥️ Screenshots

<img width="1388" height="847" alt="image" src="https://github.com/user-attachments/assets/cea503f4-109a-4a3b-93e2-d1be3ef73f42" />

<p align="center">
  <img src="./media/2026-08-29%20150559.gif" alt="Icon Generator Demo" width="900">
</p>

<p align="center">
  <img src="./media/2026-08-29 151129.gif" alt="Icon Generator Demo" width="900">
</p>

---

### 🛠️ Systemanforderungen

- **Python 3.8 oder höher**
- **Cairo / GTK3 Runtime** (für die SVG → PNG Konvertierung)

---

### 🚀 Installation und Ausführung

```bash
# 1. Repository klonen
git clone [https://github.com/your-username/icon-generator.git](https://github.com/your-username/icon-generator.git)
cd icon-generator

# 2. Abhängigkeiten installieren
pip install -r requirements.txt

# 3. Programm ausführen
python icon_generator.py
```

---

### 🙏 Danksagungen

- [Tabler Icons](https://tabler.io/icons) — Für ihre unglaubliche Open-Source-Icon-Bibliothek.
- [CairoSVG](https://cairosvg.org/) — Für die SVG zu PNG Konvertierung in Python.

</details>

<details>
<summary><h2>🇫🇷 Français (Francés)</h2></summary>

### 🎯 Qu'est-ce que c'est ?

Un outil de bureau en Python qui vous permet de **télécharger, prévisualiser et générer des icônes Tabler** dans plusieurs tailles, couleurs et épaisseurs de trait (stroke).

Parfait pour **les designers, les développeurs et toute personne** ayant besoin d'icônes pour ses projets personnels ou professionnels.

---

### ✨ Fonctionnalités principales

- 🎨 **Aperçu en temps réel** — Ajustez la taille, la couleur et le trait et voyez le résultat instantanément.
- 📥 **Téléchargement automatique des SVG** — Obtient les icônes directement depuis le CDN de Tabler Icons.
- 🖼️ **Génération en masse de PNG** — Créez des centaines d'icônes avec toutes les combinaisons dont vous avez besoin.
- 📂 **Organisation automatique** — Enregistre les PNG dans des sous-dossiers par taille et épaisseur.
- 🎯 **Sélection persistante** — Se souvient des icônes que vous avez sélectionnées entre les sessions.
- 🌍 **Multilingue** — Prise en charge de 6 langues.
- 🖱️ **Interface intuitive** — Design sombre, épuré et professionnel.
- 🆓 **Entièrement gratuit** — Open source, libre pour un usage personnel et commercial.

---

### 🖥️ Captures d'écran

<img width="1388" height="847" alt="image" src="https://github.com/user-attachments/assets/cea503f4-109a-4a3b-93e2-d1be3ef73f42" />

<p align="center">
  <img src="./media/2026-08-29%20150559.gif" alt="Icon Generator Demo" width="900">
</p>

<p align="center">
  <img src="./media/2026-08-29 151129.gif" alt="Icon Generator Demo" width="900">
</p>

---

### 🛠️ Configuration requise

- **Python 3.8 ou supérieur**
- **Cairo / GTK3 Runtime** (pour la conversion SVG → PNG)

---

### 🚀 Installation et exécution

```bash
# 1. Cloner le dépôt
git clone [https://github.com/your-username/icon-generator.git](https://github.com/your-username/icon-generator.git)
cd icon-generator

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Exécuter le programme
python icon_generator.py
```

---

### 🙏 Remerciements

- [Tabler Icons](https://tabler.io/icons) — Pour leur incroyable bibliothèque d'icônes open source.
- [CairoSVG](https://cairosvg.org/) — Pour la conversion SVG vers PNG en Python.

</details>

<details>
<summary><h2>🇯🇵 日本語 (Japonés)</h2></summary>

### 🎯 これはなんですか？

Pythonで作成されたデスクトップツールで、**Tabler Iconsのダウンロード、プレビュー、生成**を複数のサイズ、色、線の太さ（ストローク）で行うことができます。

個人または商用プロジェクトでアイコンを必要とする**デザイナー、開発者、すべての人**に最適です。

---

### ✨ 主な機能

- 🎨 **リアルタイムプレビュー** — サイズ、色、ストロークを調整し、結果を即座に確認できます。
- 📥 **SVGの自動ダウンロード** — Tabler Icons CDNから直接アイコンを取得します。
- 🖼️ **PNGの一括生成** — 必要なすべての組み合わせで何百ものアイコンを作成します。
- 📂 **自動整理** — サイズとストロークごとにサブフォルダーにPNGを保存します。
- 🎯 **選択の永続化** — セッション間で選択したアイコンを記憶します。
- 🌍 **多言語対応** — 6言語をサポート。
- 🖱️ **直感的なインターフェース** — ダークでクリーン、プロフェッショナルなデザイン。
- 🆓 **完全無料** — オープンソース。個人および商用利用無料。

---

### 🖥️ スクリーンショット

<img width="1388" height="847" alt="image" src="https://github.com/user-attachments/assets/cea503f4-109a-4a3b-93e2-d1be3ef73f42" />

<p align="center">
  <img src="./media/2026-08-29%20150559.gif" alt="Icon Generator Demo" width="900">
</p>

<p align="center">
  <img src="./media/2026-08-29 151129.gif" alt="Icon Generator Demo" width="900">
</p>

---

### 🛠️ システム要件

- **Python 3.8 以上**
- **Cairo / GTK3 Runtime** (SVG → PNG 変換用)

---

### 🚀 インストールと実行

```bash
# 1. リポジトリのクローン
git clone [https://github.com/your-username/icon-generator.git](https://github.com/your-username/icon-generator.git)
cd icon-generator

# 2. 依存関係のインストール
pip install -r requirements.txt

# 3. プログラムの実行
python icon_generator.py
```

---

### 🙏 謝辞

- [Tabler Icons](https://tabler.io/icons) — 素晴らしいオープンソースアイコンライブラリを提供していただきありがとうございます。
- [CairoSVG](https://cairosvg.org/) — PythonでのSVGからPNGへの変換を可能にしていただきありがとうございます。

</details>

<details>
<summary><h2>🇷🇺 Русский (Ruso)</h2></summary>

### 🎯 Что это?

Десктопное приложение на Python, которое позволяет вам **скачивать, просматривать и генерировать иконки Tabler** в различных размерах, цветах и с разной толщиной линий (stroke).

Идеально подходит для **дизайнеров, разработчиков и всех**, кому нужны иконки для личных или профессиональных проектов.

---

### ✨ Основные возможности

- 🎨 **Предпросмотр в реальном времени** — Настраивайте размер, цвет и толщину линий и мгновенно видите результат.
- 📥 **Автоматическая загрузка SVG** — Получает иконки напрямую с CDN Tabler Icons.
- 🖼️ **Массовая генерация PNG** — Создавайте сотни иконок со всеми необходимыми комбинациями.
- 📂 **Автоматическая организация** — Сохраняет PNG в подпапки по размеру и толщине линий.
- 🎯 **Сохранение выбора** — Запоминает выбранные вами иконки между сеансами.
- 🌍 **Мультиязычность** — Поддержка 6 языков.
- 🖱️ **Интуитивно понятный интерфейс** — Темный, чистый и профессиональный дизайн.
- 🆓 **Абсолютно бесплатно** — Открытый исходный код, бесплатно для личного и коммерческого использования.

---

### 🖥️ Скриншоты

<img width="1388" height="847" alt="image" src="https://github.com/user-attachments/assets/cea503f4-109a-4a3b-93e2-d1be3ef73f42" />

<p align="center">
  <img src="./media/2026-08-29%20150559.gif" alt="Icon Generator Demo" width="900">
</p>

<p align="center">
  <img src="./media/2026-08-29 151129.gif" alt="Icon Generator Demo" width="900">
</p>

---

### 🛠️ Системные требования

- **Python 3.8 или выше**
- **Cairo / GTK3 Runtime** (для конвертации SVG → PNG)

---

### 🚀 Установка и запуск

```bash
# 1. Клонировать репозиторий
git clone [https://github.com/your-username/icon-generator.git](https://github.com/your-username/icon-generator.git)
cd icon-generator

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Запустить программу
python icon_generator.py
```

---

### 🙏 Благодарности

- [Tabler Icons](https://tabler.io/icons) — За их невероятную библиотеку иконок с открытым исходным кодом.
- [CairoSVG](https://cairosvg.org/) — За конвертацию SVG в PNG на Python.

</details>

<details open>
<summary><h2>🇪🇸 Español (Spanish)</h2></summary>

### 🎯 ¿Qué es esto?

Una herramienta de escritorio en Python que te permite **descargar, previsualizar y generar iconos de Tabler Icons** en múltiples tamaños, colores y grosores de trazo (stroke).

Perfecta para **diseñadores, desarrolladores y cualquier persona** que necesite iconos para sus proyectos personales o profesionales.

---

### ✨ Características principales

- 🎨 **Previsualización en tiempo real** — Ajusta tamaño, color y stroke y ve el resultado al instante.
- 📥 **Descarga automática de SVGs** — Obtiene los iconos directamente desde la CDN de Tabler Icons.
- 🖼️ **Generación masiva de PNGs** — Crea cientos de iconos con todas las combinaciones que necesites.
- 📂 **Organización automática** — Guarda los PNGs en subcarpetas por tamaño y stroke.
- 🎯 **Selección persistente** — Recuerda qué iconos has seleccionado entre sesiones.
- 🌍 **Multilenguaje** — Soporte para 6 idiomas (Español, Inglés, Alemán, Francés, Japonés, Ruso).
- 🖱️ **Interfaz intuitiva** — Diseño oscuro, limpio y profesional.
- 🆓 **Completamente gratuito** — Open source, libre para uso personal y comercial.

---

### 🌍 Idiomas soportados

| Código | Idioma | Archivo |
| :---: | :--- | :--- |
| 🇪🇸 `es` | Español | `es.json` |
| 🇬🇧 `gb` | Inglés | `gb.json` |
| 🇩🇪 `de` | Alemán | `de.json` |
| 🇫🇷 `fr` | Francés | `fr.json` |
| 🇯🇵 `jp` | Japonés | `jp.json` |
| 🇷🇺 `ru` | Ruso | `ru.json` |

> **¡Puedes añadir más idiomas!** Solo crea un archivo JSON en la carpeta `language/`.

---

### 🖥️ Captura de pantalla

<img width="1388" height="847" alt="image" src="https://github.com/user-attachments/assets/cea503f4-109a-4a3b-93e2-d1be3ef73f42" />

<p align="center">
  <img src="./media/2026-08-29%20150559.gif" alt="Icon Generator Demo" width="900">
</p>

<p align="center">
  <img src="./media/2026-08-29 151129.gif" alt="Icon Generator Demo" width="900">
</p>

---

### 🛠️ Requisitos del sistema

- **Python 3.8 o superior**
- **Cairo / GTK3 Runtime** (para la conversión SVG → PNG)

---

### 📦 Instalación de dependencias

#### 1. Instalar Python

Descarga e instala Python desde [python.org](https://python.org/downloads/).

#### 2. Instalar Cairo (obligatorio)

<details>
<summary><b>Windows</b></summary>

1. Descarga el instalador de **GTK3 Runtime** desde [GTK for Windows Runtime Environment Releases](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases).
2. Ejecuta el instalador y sigue las instrucciones.
3. Reinicia tu terminal.
</details>

<details>
<summary><b>Linux (Ubuntu/Debian)</b></summary>

```bash
sudo apt-get update
sudo apt-get install libcairo2-dev libgirepository1.0-dev
```
</details>

<details>
<summary><b>Linux (Fedora)</b></summary>

```bash
sudo dnf install cairo-devel
```
</details>

<details>
<summary><b>Linux (Arch)</b></summary>

```bash
sudo pacman -S cairo
```
</details>

<details>
<summary><b>macOS</b></summary>

```bash
# Con Homebrew
brew install cairo

# Con MacPorts
sudo port install cairo
```
</details>

#### 3. Instalar dependencias de Python

📄 **requirements.txt**

```text
Pillow>=10.0.0
requests>=2.31.0
cairosvg>=2.7.0
```

Ejecuta el siguiente comando para instalar las librerías necesarias:

```bash
pip install -r requirements.txt
```

---

### 🚀 Instalación y ejecución

```bash
# 1. Clonar el repositorio
git clone [https://github.com/tu-usuario/icon-generator.git](https://github.com/tu-usuario/icon-generator.git)
cd icon-generator

# 2. Crear estructura de carpetas
mkdir icons
mkdir language

# 3. Instalar dependencias de Python
pip install -r requirements.txt

# 4. Ejecutar el programa
python icon_generator.py
```

---

### 📁 Estructura de archivos

```text
icon-generator/
├── icon_generator.py            # Archivo principal
├── requirements.txt              # Dependencias Python
├── generator_config.json         # Configuración persistente
├── icons/                        # Iconos descargados y generados
│   ├── pencil.svg               # SVGs descargados
│   ├── size_16/                 # PNGs organizados por tamaño
│   │   ├── stroke_1/
│   │   │   └── pencil_16px_accent_stroke1.png
│   │   └── stroke_2/
│   └── ...
└── language/                     # Archivos de idioma
    ├── es.json                  # Español
    ├── gb.json                  # Inglés
    ├── de.json                  # Alemán
    ├── fr.json                  # Francés
    ├── jp.json                  # Japonés
    └── ru.json                  # Ruso
```

---

### 🌍 Archivos de idioma

Los archivos de idioma deben colocarse en la carpeta `language/` con el siguiente formato:

<details>
<summary><b>Ejemplo: es.json (Español)</b></summary>

```json
{
  "_language_name": "Español",
  "app": {
    "title": "Icon Generator",
    "brand": "/ generador de iconos",
    "subtitle": "Configura y genera tus iconos"
  },
  "buttons": {
    "generate": "🚀 Generar iconos",
    "generating": "⏳ Generando...",
    "add": "Añadir",
    "delete": "Eliminar",
    "all": "Todos",
    "none": "Ninguno",
    "change": "Cambiar",
    "cancel": "Cancelar",
    "select_all": "✅ Seleccionar todos",
    "deselect_all": "❌ Deseleccionar todos",
    "add_icon": "➕ Añadir icono",
    "change_variant": "🔄 Cambiar variante",
    "remove_icon": "✖ Eliminar icono",
    "tabler_list": "📋 Lista Tabler",
    "view_tabler": "🌐 Ver todos en tabler.io"
  },
  "ui": {
    "preview": "Previsualización",
    "size": "Tamaño:",
    "color": "Color:",
    "background": "Fondo:",
    "stroke": "Stroke:",
    "search": "Buscar:",
    "sizes": "Tamaños:",
    "colors": "Colores:",
    "filter": "🔍 Filtrar:",
    "icons_count": "Iconos ({count})",
    "additional_icons": "━━━ Iconos adicionales ━━━"
  },
  "colors": {
    "accent": "Acento",
    "muted": "Muted",
    "text": "Texto",
    "red": "Rojo",
    "green": "Verde",
    "blue": "Azul",
    "orange": "Naranja",
    "purple": "Morado",
    "pink": "Rosa",
    "teal": "Verde azulado",
    "yellow": "Amarillo",
    "cyan": "Cian",
    "white": "Blanco",
    "black": "Negro"
  },
  "background": {
    "black": "Negro",
    "white": "Blanco",
    "dark_gray": "Gris oscuro",
    "light_gray": "Gris claro",
    "surface": "Superficie",
    "color_prefix": "Fondo: "
  },
  "sections": {
    "generation_config": "Configuración de generación",
    "console": "Consola"
  },
  "options": {
    "overwrite": "Sobrescribir archivos existentes",
    "organize": "Organizar en subcarpetas por tamaño"
  },
  "dialogs": {
    "tabler_title": "📋 Selector de iconos de Tabler",
    "tabler_select": "Selecciona un icono de la lista (con previsualización):",
    "custom_title": "➕ Añadir icono personalizado",
    "custom_select": "Busca y selecciona un icono:",
    "change_variant_title": "{emoji} Cambiar variante de '{icon}'",
    "change_variant": "Selecciona una variante para '{icon}':",
    "choose_color": "Selecciona un color",
    "color_name_title": "Nombre del color",
    "color_name": "Nombre del color:"
  },
  "messages": {
    "error": "Error",
    "warning": "Advertencia",
    "info": "Información",
    "confirm": "Confirmar",
    "select_icon": "Selecciona un icono",
    "not_found": "No encontrado",
    "already_in_list": "'{icon}' ya está en la lista",
    "icon_exists": "El icono '{icon}' ya existe",
    "base_icon_warning": "'{icon}' es un icono base necesario para la aplicación.\nNo se puede eliminar.",
    "confirm_remove_icon": "¿Eliminar el icono '{icon}'?",
    "select_color_to_remove": "Selecciona al menos un color para eliminar",
    "cannot_remove_accent": "No se puede eliminar 'Accent (Lima)'",
    "confirm_remove_colors": "¿Eliminar {count} colores?",
    "no_icons": "No hay iconos disponibles.\nAñade iconos usando el botón '➕ Añadir icono'.",
    "icon_not_found": "'{icon}' no encontrado",
    "select_requirements": "Selecciona al menos un icono, tamaño, color y stroke"
  },
  "status": {
    "loading_icons": "Cargando iconos...",
    "generation_summary": "📊 {icons} iconos × {sizes} tamaños × {colors} colores × {strokes} strokes = {total} archivos"
  },
  "logs": {
    "downloading": "📥 Descargando iconos...",
    "icons_ready": "✅ Iconos listos!",
    "icon_downloaded": "  ✅ {icon}.svg descargado",
    "icon_http_error": "  ❌ {icon}.svg (HTTP {status})",
    "icon_http_error_short": "  ❌ {icon}.svg (HTTP {status})",
    "download_error": "  ❌ Error descargando {icon}: {error}",
    "download_error_short": "  ❌ {icon}.svg ({error})",
    "icon_added": "✅ Icono añadido: {icon}",
    "icon_changed": "🔄 Icono cambiado: {old} → {new}",
    "icon_removed": "🗑️ Icono eliminado: {icon}",
    "color_added": "✅ Color añadido: {name} ({color})",
    "colors_removed": "🗑️ Eliminados {count} colores",
    "generating": "🚀 Generando iconos...",
    "icons_count": "📦 Iconos: {count}",
    "sizes": "📐 Tamaños: {values}",
    "colors": "🎨 Colores: {values}",
    "strokes": "📏 Strokes: {values}",
    "generated_progress": "  ✅ {count} archivos generados...",
    "generated": "✅ Generados {count} iconos",
    "generation_errors": "⚠️ {count} errores"
  },
  "search": {
    "placeholder": "Escribe para filtrar..."
  },
  "color": {
    "default_name": "Color_{number}"
  },
  "language": {
    "label": "Idioma:"
  }
}
```
</details>

---

### 🙏 Agradecimientos

- [Tabler Icons](https://tabler.io/icons) — Por su increíble biblioteca de iconos open source.
- [CairoSVG](https://cairosvg.org/) — Por la conversión de SVG a PNG en Python.

</details>
