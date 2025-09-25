# File Encryptor
A minimal cross-platform GUI app for encrypting and decrypting files.

## Features
- Encrypt any file → saves alongside the input with the .encr suffix.
- Decrypt a previously encrypted file → restores the original filename.
- Always saves next to the input file.
- Thread-safe GUI — all updates are routed to the main thread.

## Installation
1) Clone the repo
```bash
git clone https://github.com/dddiias/file-encryption-gui.git
cd file-encryption-gui
```
2) Create & activate a virtual environment
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
```
3) Install dependencies
```bash
pip install -r requirements.txt
```

## Quick Start
```bash
python -m app.main
```

### Steps:
1) Input file — choose a file.
2) Mode — Encrypt or Decrypt.
3) Password — enter a password.
4) Start — run the operation.
    - Encrypt → creates name.ext.encr next to the input.
    - Decrypt → for name.ext.encr, restores name.ext.