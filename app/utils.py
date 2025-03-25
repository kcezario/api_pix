# app/utils.py
from app.inter_pix import get_access_token, efetuar_pagamento_pix, consultar_pagamento
import uuid

def show_option_menu():
    print("=========================================")
    print("|            MENU DE OPÇÕES             |")
    print("=========================================")
    print("| Opções:                               |")
    print("|   1 - Realizar pagamento              |")
    print("|   2 - Consultar status do pagamento   |")
    print("=========================================")
    
    escolha = input("Digite o número da opção desejada e pressione Enter: ")

    # Obter token de acesso
    token = get_access_token()
    
    if escolha == "1":
        # Opção 1: Realizar pagamento
        txid = str(uuid.uuid4())[:35]  # Gerar um txid único
        valor = input("Digite o valor do pagamento (ex: 10.00): ").strip()
        chave_destino = input("Digite a chave Pix do destinatário: ").strip()
        descricao = input("Digite a descrição do pagamento: ").strip()

        pagamento = efetuar_pagamento_pix(
            access_token=token,
            txid=txid,
            valor=valor,
            chave_destino=chave_destino,
            descricao=descricao
        )
        print("Pagamento realizado com sucesso:", pagamento)
        
    elif escolha == "2":
        # Opção 2: Consultar status do pagamento
        txid = input("Digite o TXID do pagamento: ").strip()
        
        status = consultar_pagamento(token, txid)
        print("Status do pagamento:", status)
        
    else:
        print("Opção inválida. Por favor, digite '1' para pagamento ou '2' para consultar o status.")
