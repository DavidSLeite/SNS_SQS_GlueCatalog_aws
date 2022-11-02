import json
from datetime import datetime
import pandas as pd
import awswrangler as wr
import logging
import os


def lambda_handler(event, context):
    inicioLambda = str(datetime.now())
    
    # Gera log personalizado para o cloudwatch
    def geraLog(msg):
        logging.basicConfig(format='%(message)s')
        logger = logging.getLogger('lambda_handler')
        logger.setLevel('INFO')
        logger.info(json.dumps(msg))
    
    # Gera dataframe com os dados de evento
    def criaDF(event):
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
        
        df = pd.json_normalize(event, max_level = None, sep = '_')
        
        return df

    # Insere os dados do dataframe pandas na tabela Glue Catalog, criando partições dinamicamente pela lib awswrangler
    def exec_df_to_table(
        df,
        path,
        database,
        table,
        partition_cols,
        dtype,
        msg
    ):
        try:
            execute = wr.s3.to_parquet(
                df = df,
                path = path,
                dataset = True,
                mode = 'append',
                database = database,
                table = table,
                partition_cols=partition_cols,
                dtype = dtype
            )
            
            msg['end-execution'] = str(datetime.now())
            msg['status-execution'] = 'sucess'
            msg['sucess-message'] = execute
            return msg
        except Exeption as error:
            msg['end-execution'] = str(datetime.now())
            msg['status-execution'] = 'error'
            msg['error-message'] = error
            return msg
            
    # Vars de inicialização
    df = criaDF(event)
    path = os.environ['PATH_S3']
    partition_cols = ['data_transacao']
    database = 'dbtransacaocorp'
    table = 'tb_transacao_pix'
    dtype = {
        'identificador_transacao': 'string',
        'data_hora_transacao': 'string',
        'conta_origem_numero_agencia': 'string',
        'conta_origem_numero_conta': 'string',
        'conta_origem_dict': 'string',
        'conta_origem_tipo_conta': 'string',
        'conta_origem_identificador_cliente': 'string',
        'conta_origem_tipo_chave_origem': 'string',
        'conta_origem_chave_pix_origem': 'string',
        'conta_origem_descricao_transacao': 'string',
        'conta_origem_nome_cliente': 'string',
        'conta_destino_numero_agencia': 'string',
        'conta_destino_numero_conta': 'string',
        'conta_destino_dict': 'string',
        'conta_destino_tipo_conta': 'string',
        'conta_destino_identificador_cliente': 'string',
        'conta_destino_tipo_chave_destino': 'string',
        'conta_destino_chave_pix_destino': 'string',
        'valor_transacao': 'string',
        'tipo_moeda': 'string',
        'data_transacao': 'string'
    }
    
    # dicionário para mensagem personalizada
    msg = {
        'type' : 'lambda',
        'lambda-function' : 'lambda_process_fila_transacao_pix',
        'start-execution' : inicioLambda
    }
    
    msg = exec_df_to_table(
        df,
        path,
        database,
        table,
        partition_cols,
        dtype,
        msg
    )
    
    #logar a execução do lambda no cloudwatch
    geraLog(msg)