import threading
from typing import Optional, Dict, Any, Tuple
import PySimpleGUI.PySimpleGUI as sg
from .fs import encrypt_file, decrypt_file

EVT_PROGRESS = "-EVT-PROGRESS-"
EVT_DONE     = "-EVT-DONE-"
EVT_ERROR    = "-EVT-ERROR-"

class Worker:
    def __init__(self, window: sg.Window):
        self._win = window
        self._th: Optional[threading.Thread] = None
        self._cancel = threading.Event()

    def busy(self) -> bool:
        return self._th is not None and self._th.is_alive()

    def cancel(self):
        self._cancel.set()

    def run_task(self, fn, args: Tuple, context: Dict[str, Any]):
        if self.busy():
            return
        self._cancel.clear()

        def _prog(processed: int, total: int):
            pct = int(processed * 100 / total) if total else 100
            self._win.write_event_value(EVT_PROGRESS, {"pct": pct, "processed": processed, "total": total})

        def target():
            try:
                fn(*args, progress_cb=_prog, is_cancelled=self._cancel.is_set)
                self._win.write_event_value(EVT_DONE, context)
            except Exception as e:
                self._win.write_event_value(EVT_ERROR, {"error": str(e), **context})

        self._th = threading.Thread(target=target, daemon=True)
        self._th.start()

def pick_output_path(input_path: str, decrypt: bool, out_dir: Optional[str], save_same: bool) -> str:
    import os
    if save_same or not out_dir:
        if decrypt:
            return input_path[:-5] if input_path.endswith(".encr") else input_path + ".out"
        return input_path + ".encr"
    base = os.path.basename(input_path)
    if decrypt and base.endswith(".encr"):
        base = base[:-5]
    elif not decrypt:
        base = base + ".encr"
    return os.path.join(out_dir, base)
