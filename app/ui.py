import PySimpleGUI.PySimpleGUI as sg

def _safe_theme(name: str = "SystemDefault"):
    if hasattr(sg, "set_options"):
        try:
            sg.set_options(font=None)
        except Exception:
            pass
    if hasattr(sg, "theme"):
        try:
            sg.theme(name)
        except Exception:
            pass

def make_window():
    _safe_theme("SystemDefault")

    layout = [
        [sg.Text("Input file"),
         sg.Input(key="-IN-", enable_events=True, expand_x=True),
         sg.FileBrowse("Browse...")],

        [sg.Text("Mode"),
         sg.Radio("Encrypt", "MODE", key="-MODE-ENC-", default=True),
         sg.Radio("Decrypt", "MODE", key="-MODE-DEC-")],

        [sg.Text("Password"),
         sg.Input(password_char="*", key="-PWD-", expand_x=True)],

        [sg.ProgressBar(max_value=100, orientation="h", size=(40, 10), key="-PROGRESS-")],

        [sg.Multiline(size=(80, 12), key="-LOG-", autoscroll=True,
                      disabled=True, expand_x=True, expand_y=True)],

        [sg.Button("Start", key="-START-"),
         sg.Button("Cancel", key="-CANCEL-", disabled=True),
         sg.Button("Exit")],
    ]

    win = sg.Window("File Encryptor (educational)", layout,
                    resizable=True, finalize=True)
    return win
