# Activation Code Generator

A powerful and user-friendly activation code generation tool with batch generation, custom formatting, duplicate checking, and more features.

## Features

- 🎯 **Flexible Activation Code Format**: Customizable segments, segment length, and delimiter
- 📦 **Batch Generation**: Supports generating 1-100,000 activation codes with fast generation mode
- 🔍 **Duplicate Detection**: Automatically detects and alerts duplicate activation codes
- 💾 **Smart Saving**: Supports saving to file, save as, and auto-save
- 🎨 **Friendly Graphical Interface**: Modern GUI based on wxPython
- 🔧 **Rich Setting Options**: Customizable character set, save path, etc.
- ⚡ **Fast Generation Mode**: Optimizes generation speed for large batches of activation codes
- 🌍 **Multi-language Support**: Supports Simplified Chinese, English, Spanish, Hindi, Arabic, Portuguese, Russian, Japanese, German, and French
- 🚀 **Cross-platform Support**: Includes startup scripts for Windows, Linux, and macOS
- 🛠️ **Auto Environment Detection**: Automatically detects and installs Python and dependencies

## Installation Instructions

### Environment Requirements

- Python 3.6+
- wxPython

### Installation Steps

1. **Clone the project**

```bash
git clone https://github.com/zhangleyan0413/activation-code-generator.git
cd activation-code-generator
```

2. **Install dependencies**

```bash
pip install wxPython
```

3. **Run the program**

```bash
# Windows
run.bat

# Linux
chmod +x run.sh
./run.sh

# macOS
chmod +x run.command
./run.command

# Or run directly
python main.py
```

## Usage Guide

### Basic Usage

1. **Generate Activation Codes**
   - Enter the number of activation codes to generate in the main interface
   - Click the "Generate Codes" button
   - The generated activation codes will be displayed in the text box below

2. **Save Activation Codes**
   - Click the "Save to File" button
   - Activation codes will be saved to the `激活码.txt` file

### Advanced Features

1. **Batch Generation**
   - Open the batch generation dialog through the menu "Tools → Batch Generate..."
   - Set the generation quantity (up to 100,000)
   - Select whether to use fast generation mode
   - Click the "Generate" button

2. **Custom Settings**
   - Open the settings dialog through the menu "Tools → Settings..."
   - Customize activation code format, character set, save path, etc.
   - Click "OK" to save settings

3. **Save As**
   - Open the save as dialog through the menu "File → Save As..."
   - Select save path and file name
   - Click the "Save" button

4. **Open File**
   - Open an activation code file through the menu "File → Open..."
   - The program will automatically detect duplicate activation codes in the file

## Interface Preview

![Main Interface](images/prtsc1.png)

![Batch Generation](images/prtsc2.png)

![Settings Interface](images/prtsc3.png)

## Activation Code Format

Default format: `XXXXX-XXXXX-XXXXX-XXXXX`

- 5 characters per segment
- Uses `-` as delimiter
- Includes numbers and uppercase letters

Custom formats are supported:
- 1-10 activation code segments
- 1-10 characters per segment
- Custom delimiters
- Optional character sets (numbers, uppercase/lowercase letters, special characters)

## Save Format

Activation codes will be saved in the following format:

```
生成时间：2026-02-20 12:00:00
生成个数：10
ABCDE-12345-FGHIJ-KLMNO
PQRST-67890-UVWXY-ZABCD
...
--------------------------------------------------
```

## Contribution Guide

Contributions and issues are welcome!

1. Fork this project
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Contact

- Author: myiunagn
- Email: myiunagn@outlook.com
- Project link: https://github.com/zhangleyan0413/activation-code-generator

## Changelog

### v1.1.0
- ✨ Added multi-language support, supporting the top 10 most used languages in the world
- 🚀 Added cross-platform startup scripts (Windows, Linux, macOS)
- 🛠️ Added auto environment detection, automatically installing Python and dependencies
- 🎨 Optimized interface text to ensure all pages support multiple languages
- ✨ Increased batch generation limit to 100,000,000,000
- 🎯 Improved settings dialog, supporting language switching

### v1.0.2
- ✨ Added fast generation mode to optimize generation speed for large batches of activation codes
- ✨ Added save as functionality
- 🐛 Fixed garbled code issues
- 🎨 Improved batch generation dialog

### v1.0.1
- ✨ Added duplicate detection functionality
- ✨ Added menu bar
- 🎨 Improved interface layout

### v1.0.0
- 🎉 Initial version release
- ✨ Basic activation code generation functionality
- ✨ Batch generation functionality
- ✨ Save to file functionality
