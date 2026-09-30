import subprocess
import time
import os

def gerar_lista_teste(nome_ficheiro, quantidade):
    with open(nome_ficheiro, "w") as f:
        for i in range(quantidade):
            f.write(f"{1000 + i}\n")

def contar_linhas(nome_ficheiro):
    if not os.path.exists(nome_ficheiro):
        return 0
    with open(nome_ficheiro, "r") as f:
        return sum(1 for _ in f)

def executar_p1(ficheiro_ids, num_threads, nome_log):
    inicio = time.time()
    
    # Limpa o log anterior
    if os.path.exists(nome_log):
        os.remove(nome_log)
        
    # Cria o processo P1
    processo = subprocess.run(
        ["python", "p1.py", ficheiro_ids, str(num_threads), nome_log],
        capture_output=True
    )
    
    fim = time.time()
    tempo_total = fim - inicio
    
    # Auditoria
    ids_esperados = contar_linhas(ficheiro_ids)
    linhas_log = contar_linhas(nome_log)
    
    status = "Sucesso"
    if processo.returncode != 0:
        status = f"Erro (Código {processo.returncode})"
    elif ids_esperados != linhas_log:
        status = "Enriquecimento incompleto"
        
    return tempo_total, status

def main():
    testes = [
        {"tamanho": "Pequena", "qtd": 50},
        {"tamanho": "Média", "qtd": 500},
        {"tamanho": "Grande", "qtd": 2000}
    ]
    
    n_threads_multi = 4 # Podes ajustar este valor
    resultados = []
    
    print(f"{'Tamanho':<10} | {'IDs':<5} | {'Threads':<7} | {'Tempo (s)':<10} | {'Status'}")
    print("-" * 60)
    
    for teste in testes:
        ficheiro_ids = f"lista_ids_{teste['tamanho'].lower()}.txt"
        nome_log = f"log_{teste['tamanho'].lower()}.txt"
        
        gerar_lista_teste(ficheiro_ids, teste['qtd'])
        
        # Execução com N=1
        t_seq, status_seq = executar_p1(ficheiro_ids, 1, nome_log)
        print(f"{teste['tamanho']:<10} | {teste['qtd']:<5} | {1:<7} | {t_seq:<10.4f} | {status_seq}")
        resultados.append((1, teste['tamanho'], t_seq, status_seq))
        
        # Execução com N>1
        t_par, status_par = executar_p1(ficheiro_ids, n_threads_multi, nome_log)
        print(f"{teste['tamanho']:<10} | {teste['qtd']:<5} | {n_threads_multi:<7} | {t_par:<10.4f} | {status_par}")
        resultados.append((n_threads_multi, teste['tamanho'], t_par, status_par))

if __name__ == "__main__":
    main()