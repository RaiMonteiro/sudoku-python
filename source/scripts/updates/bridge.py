# This bridge.py file serves as a "bridge" between the update process and the game running.
import os, sys
import subprocess

def launch():
        try:
            exe_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "Sudoku.exe")
            subprocess.Popen([exe_path], cwd=os.path.dirname(exe_path))
        except Exception as e:
            with open("source/scripts/updates/launcher_log.txt", mode="w", encoding="utf-8") as log:
                log.write(f"ERROR: {str(e)}\nFailed game start or Corrupted path in {exe_path}")

if __name__ == "__main__":
    launch()
    sys.exit()