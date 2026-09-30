import sys
import json
import threading
import time
from datetime import datetime
import random

# P1 recebe parâmetros passados pelo P0
if len(sys.argv) != 4:
    print("Uso: python p1.py <lista_ids.txt> <num_threads> <arquivo_log>")
    sys.exit(1)

arquivo_entrada = sys.argv[1]
num_threads = int(sys.argv[2])
arquivo_log = sys.argv[3]

try:
    with open(arquivo_entrada, 'r') as f:
        # Carrega IDs na memória
        ids = [linha.strip() for linha in f if linha.strip()]
except Exception as e:
    sys.exit(2)

# Exclusão Mútua (Mutex) exigida nos requisitos
mutex_lista = threading.Lock()
mutex_log = threading.Lock()

def mock_api(id_val):
    """Simula a API mockada que devolve dados em formato JSON"""
    time.sleep(random.uniform(0.01, 0.05)) # Simula latência de rede
    # Resposta na estrutura fixa JSON válida
    return json.dumps({"id": int(id_val), "status": "ok", "valor": round(random.uniform(100, 1000), 2)})

def worker(thread_name):
    """Função executada por cada thread."""
    while True:
        # Mutex na lista: Garante que cada ID seja processado exatamente uma vez (nenhuma duplicidade)
        with mutex_lista:
            if not ids:
                break
            id_atual = ids.pop(0)

        # Consulta a API fora do Lock para permitir o paralelismo real entre as threads
        resposta_json = mock_api(id_atual)
        data_execucao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        linha_log = f"{data_execucao}, {thread_name}, {id_atual}, {resposta_json}\n"
        
        # Mutex no Log: Protege a escrita concorrente no arquivo
        with mutex_log:
            with open(arquivo_log, 'a') as f:
                f.write(linha_log)

# Limpa o arquivo de log a cada nova execução
with open(arquivo_log, 'w') as f:
    pass

# Criação de N threads de trabalho
threads = []
for i in range(num_threads):
    t = threading.Thread(target=worker, args=(f"Thread-{i+1}",))
    threads.append(t)
    t.start()

# Aguarda a finalização de todas as threads
for t in threads:
    t.join()

# Termina com sucesso
sys.exit(0)