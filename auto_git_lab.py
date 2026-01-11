import os
import shutil
import subprocess
from datetime import datetime

# Configurações
SOURCE_DIR = os.path.expanduser("~/meu-laboratorio-cyber") # Onde ficam as capturas
REPO_DIR = os.path.expanduser("~/site-dgprograma")        # Pasta do seu repositório Git
TARGET_SUBDIR = "capturas_arquivadas"                      # Pasta dentro do repo

def organizar_e_subir():
    # 1. Criar pasta com a data de hoje para organização
    hoje = datetime.now().strftime("%Y-%m-%d")
    destino = os.path.join(REPO_DIR, TARGET_SUBDIR, hoje)
    
    if not os.path.exists(destino):
        os.makedirs(destino)
        print(f"✅ Pasta {hoje} criada.")

    # 2. Mover ficheiros de captura (.cap, .csv, .kismet)
    extensoes = ('.cap', '.csv', '.kismet', '.log')
    ficheiros_movidos = 0
    
    for arquivo in os.listdir(SOURCE_DIR):
        if arquivo.endswith(extensoes):
            shutil.move(os.path.join(SOURCE_DIR, arquivo), os.path.join(destino, arquivo))
            ficheiros_movidos += 1
    
    if ficheiros_movidos == 0:
        print("⚠️ Nenhum ficheiro novo para organizar.")
        return

    # 3. Comandos Git automáticos
    try:
        os.chdir(REPO_DIR)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Automação: {ficheiros_movidos} novas capturas em {hoje}"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print(f"🚀 Sucesso! {ficheiros_movidos} ficheiros enviados para o GitHub.")
    except Exception as e:
        print(f"❌ Erro no Git: {e}")

if __name__ == "__main__":
    organizar_e_subir()
