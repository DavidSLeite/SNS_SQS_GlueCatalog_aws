import json
from datetime import datetime
import pandas as pd

def lambda_handler(event, context):
    
    
    # Acessanto o primeiro item da lista do evento gerado pela fila SQS
    event = event['Records'][0]['body']
    
    # Convertendo conteúdo texto para dictionary 
    event = json.loads(event)
    
    # Acessando chave 'Message' do dictionary
    event = event['Message']
    
    # Convertendo conteúdo texto para dictionary 
    event = json.loads(event)
    
    # Cria var data a partir do evento
    date = datetime.strptime(event['data_hora_transacao'], '%Y-%m-%d %H:%M:%S.%f').date()
    date = str(date)
    
    # Inserindo chave data_transacao
    event['data_transacao'] = date
    
    print('print do dict')
    print(event)
    
    df = pd.json_normalize(event, max_level = None, sep = '_')
    
    print('print df')
    print(df.info)
