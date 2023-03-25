# Ingestão de dados
Este repositório tem como objetivo apresentar um exemplo de ingestão de dados que chegam numa fila sqs para uma tabela no Glue Catalog.

## Desenho de solução
![](https://github.com/DavidSLeite/pjl_de_aws/blob/main/desenho_arquitetura/Desenho%20de%20Solu%C3%A7%C3%A3o.jpg?raw=true)

## Exemplo app python que envia Mensagem para o tópico SNS
* app/Ingestao_via_sns.py

## Exemplo código python para ser usado no AWS Lambda
* lambda_function/app/lambda_process_fila_transacao_pix.py
