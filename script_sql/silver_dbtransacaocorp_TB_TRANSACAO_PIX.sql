CREATE DATABASE silver_dbtransacaocorp;

CREATE EXTERNAL TABLE IF NOT EXISTS `silver_dbtransacaocorp`.`TB_TRANSACAO_PIX` (
  `identificador_transacao` string,
  `data_hora_transacao` timestamp,
  `conta_origem_numero_agencia` string,
  `conta_origem_numero_conta` string,
  `conta_origem_dict` string,
  `conta_origem_tipo_conta` string,
  `conta_origem_identificador_cliente` string,
  `conta_origem_tipo_chave_origem` string,
  `conta_origem_chave_pix_origem` string,
  `conta_origem_descricao_transacao` string,
  `conta_origem_nome_cliente` string,
  `conta_destino_numero_agencia` string,
  `conta_destino_numero_conta` string,
  `conta_destino_dict` string,
  `conta_destino_tipo_conta` string,
  `conta_destino_identificador_cliente` string,
  `conta_destino_tipo_chave_destino` string,
  `conta_destino_chave_pix_destino` string,
  `valor_transacao` double,
  `tipo_moeda` string
)
PARTITIONED BY (`data_transacao` date)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION 's3://...'
TBLPROPERTIES ('classification' = 'parquet');