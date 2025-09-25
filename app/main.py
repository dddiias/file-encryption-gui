import os
import PySimpleGUI.PySimpleGUI as sg
from .ui import make_window
from .controller import Worker, pick_output_path, EVT_PROGRESS, EVT_DONE, EVT_ERROR
from .fs import encrypt_file, decrypt_file

def log(win, msg: str):
    win["-LOG-"].update(value=str(msg) + "\n", append=True)

def set_busy(win, busy: bool):
    win["-START-"].update(disabled=busy)
    win["-CANCEL-"].update(disabled=not busy)

def main():
    win = make_window()
    worker = Worker(win)

    while True:
        event, values = win.read(timeout=200)

        if event in (sg.WIN_CLOSED, "Exit"):
            if worker.busy():
                sg.popup_ok("Task is running. Cancel first.")
                continue
            break

        if event == "-START-":
            path = (values["-IN-"] or "").strip()
            if not path:
                sg.popup_error("Choose input file")
                continue
            pwd = values["-PWD-"]
            if not pwd:
                sg.popup_error("Enter password")
                continue

            decrypt = bool(values["-MODE-DEC-"])

            if decrypt and not path.endswith(".encr"):
                sg.popup_error("Selected file is not '.encr'. Choose an encrypted file.")
                continue

            out = pick_output_path(path, decrypt, out_dir=None, save_same=True)

            if os.path.exists(out):
                if sg.popup_yes_no(f"Output file exists:\n{out}\nOverwrite?") != "Yes":
                    log(win, "Cancelled by user (overwrite not confirmed)")
                    continue

            set_busy(win, True)
            win["-PROGRESS-"].update(0)
            log(win, f"Starting {'decrypt' if decrypt else 'encrypt'}")

            if decrypt:
                worker.run_task(decrypt_file, (path, out, pwd), {"out": out, "mode": "decrypt"})
            else:
                worker.run_task(encrypt_file, (path, out, pwd), {"out": out, "mode": "encrypt"})

        elif event == "-CANCEL-":
            if worker.busy():
                worker.cancel()
                log(win, "Cancellation requested...")

        elif event == EVT_PROGRESS:
            data = values[EVT_PROGRESS]
            win["-PROGRESS-"].update(int(data.get("pct", 0)))

        elif event == EVT_DONE:
            set_busy(win, False)
            out = values[EVT_DONE].get("out")
            log(win, f"Done. Output: {out}")
            sg.popup_ok("Completed")

        elif event == EVT_ERROR:
            set_busy(win, False)
            err = values[EVT_ERROR].get("error", "Unknown error")
            log(win, f"ERROR: {err}")
            sg.popup_error(f"Error: {err}")

    win.close()

if __name__ == "__main__":
    main()
