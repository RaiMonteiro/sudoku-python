# This file is responsible for the game's automatic update system through github
import os
import ctypes
import subprocess
import requests
import zipfile
import json

def msgbox(text: str, title: str, style: int, icon: int): return ctypes.windll.user32.MessageBoxW(0, text, title, style|icon)

def checkForUpdates():
    try:
        version_url = requests.get("https://raw.githubusercontent.com/RaiMonteiro/sudoku-python/refs/heads/main/source/r_notes/notes.json")
        online = True
    except requests.exceptions.RequestException:
        online = False
    
    if online:
        if version_url.status_code == 200: # the file was found
            # loads the remote and local json data
            remote_data = version_url.json()
            with open("source/r_notes/notes.json", mode="r", encoding="utf-8") as file: local_data = json.load(file)

            if remote_data["update"][-1]["version"] != local_data["update"][-1]["version"]: # compare versions
                if msgbox(f"Existe uma nova versão!\nPretende atualizar o jogo para a versão {remote_data["update"][-1]["version"]}?", "Sudoku Updater", 4, 0x20) == 6: # ok = 6
                    if updateFiles(remote_data["update"][-1]["version"]):
                        try:
                            exe_path = os.path.join(os.path.dirname(__file__), "launcher.exe")
                            subprocess.Popen([exe_path], cwd=os.path.dirname(exe_path)) # launch the executable
                            return "UPDATE_SUCESS"
                        
                        except FileNotFoundError:
                            msgbox(f"Arquivo não encontrado em {exe_path}.", f"Sudoku Updater - Erro: FileNotFoundError", 0, 0x30)
                            return "UPDATE_FAILED"
                        except PermissionError:
                            msgbox(f"Sem permissão para executar.", f"Sudoku Updater - Erro: PermissionError", 0, 0x30)
                            return "UPDATE_FAILED"
                        except Exception as e:
                            msgbox(f"Ocorreu um erro ao executar o programa.", f"Sudoku Updater - Erro: {str(e)}", 0, 0x30)
                            return "UPDATE_FAILED"
                        
                    else: return "UPDATE_FAILED"
                else: return "UPDATE_DECLINED"
            else: return "NO_UPDATE"
        else:
            msgbox(f"Ocorreu um erro ao verficar novas atualizações.\nPor favor tente mais tarde.", f"Sudoku Updater - Erro: {version_url.status_code}", 0, 0x30)
            return "OFFLINE"

def updateFiles(version: str):
    zip_url = f"https://github.com/RaiMonteiro/sudoku-python/releases/download/v{version}/sudoku-update-v{version}.zip"
    response = requests.get(zip_url)

    if response.status_code != 200:
        msgbox(f"Ocorreu um erro durante a atualização.\nPor favor tente mais tarde.", f"Sudoku Updater - Erro: {response.status_code}", 0, 0x30)
        return False
    
    try:
        # Open a local file in binary mode for writing, 'wb' = write binary (required for ZIP files)
        with open("update.zip", "wb") as f: f.write(response.content)

        # Open the ZIP file to extract its contents
        with zipfile.ZipFile("update.zip", 'r') as zip_ref: zip_ref.extractall(".")
            
        os.remove("update.zip") # Clean up downloaded zip
        return True
    except Exception as e:
        msgbox(f"Ocorreu um erro durante a atualização dos ficheiros locais.\nPor favor tente mais tarde.", f"Sudoku Updater - Erro: {str(e)}", 0, 0x30)
        return False