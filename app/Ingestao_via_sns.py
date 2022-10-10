import json
import uuid
import boto3
from datetime import datetime
from envVars import ARN_TOPIC_SNS

# Vars de entrada
dataHoraTransacao = datetime.now()
numeroAgenciaDestino = str(input("Digite o Número da Agencia: "))
numeroContaDestino = str(input("Digite o Número da Conta: "))
numeroDigitoContaDestino = str(input("Digite o Dígito da Conta: "))
print("========================================================")
print(
    """
    Digite o Tipo da Chave pix
        1 - CPF       
        2 - E-mail    
        3 - Celular   
    """
)
tipoChavePix = int(input("Digite aqui: "))
ChavePix = str(input("Digite a Chave Pix: "))
valorPix = float(input("Digite o Valor: "))
print("========================================================")

# Tratamento Paylaod
payload = {
    "identificador_transacao":str(uuid.uuid4()),
    "data_hora_transacao":dataHoraTransacao,
    "conta_origem":{
        "numero_agencia":"001",
        "numero_conta":"0001",
        "dict":"1",
        "tipo_conta":"Conta Corrente",
        "identificador_cliente":"1",
        "tipo_chave_origem":"email",
        "chave_pix_origem":"exemplo@exemplo.com.br",
        "descricao_transacao":"oii tudo bom, recebeu o pix? me manda msg no whats mano.",
        "nome_cliente":"Rafael Carlos dos Santos"
    },
    "conta_destino":{
        "numero_agencia":numeroAgenciaDestino,
        "numero_conta":numeroContaDestino,
        "dict":numeroDigitoContaDestino,
        "tipo_conta":"Conta Corrente",
        "identificador_cliente":"1",
        "tipo_chave_destino":tipoChavePix,
        "chave_pix_destino":ChavePix,
    },
    "valor_transacao":valorPix,
    "tipo_moeda":"BRL"
}

# payload tratado para json
payload_json = json.dumps(payload)

# Criando client AWS SNS
client = boto3.client('sns')

# publicando menssagem no topic SNS
response = client.publish(
    TargetArn = ARN_TOPIC_SNS,
    Message = json.dumps({'default': payload_json}),
    MessageStructure = 'json'
)
