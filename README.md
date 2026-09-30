<img width="1022" height="346" alt="image" src="https://github.com/user-attachments/assets/d9f3853f-5eac-4655-8ad1-7b5efa214231" />


### 2. Análise e Observações

A execução do programa comprovou um ganho prático e direto de desempenho ao escalar a aplicação de uma para múltiplas threads, especialmente notável no lote grande de 2000 identificadores (redução de ~62 segundos para ~15 segundos). O estrangulamento (gargalo) principal do sistema foi, como esperado, vinculado ao tempo de espera das requisições (I/O-bound), provocado pela latência randômica da API mockada (entre 0.01 e 0.05 segundos por requisição).

A exclusão mútua implementada não gerou limitação significativa ao paralelismo do sistema. Ao isolar a região crítica exclusivamente para as operações rápidas — a retirada do índice da lista na memória (`ids.pop(0)`) e a gravação atômica da linha no arquivo físico — as threads são bloqueadas apenas por frações de milissegundo. A operação mais custosa (chamada da API) roda de forma completamente desacoplada e simultânea fora dos blocos `with mutex`, permitindo que o escalonador do sistema operacional maximize o uso do tempo livre da CPU. Enquanto uma thread aguarda a resposta da "rede", outras assumem o processador para realizar as suas próprias requisições simultaneamente.
