## O projeto
O InFlow é um projeto de Engenharia de Dados voltado à ingestão e organização de dados públicos do Senado Federal. A proposta é preparar uma base que permita investigar despesas e atividade parlamentar.

## Perguntas que orientam o trabalho
- Qual é a despesa média mensal por senador?
- Como as despesas variam entre partidos e unidades da federação?
- Quais categorias de despesa ajudam a explicar os valores observados?
- Como identificar registros de despesa atípicos?

## Base de implementação
O trabalho parte de fontes públicas em JSON e XML, com PostgreSQL para armazenar e consultar dados e Docker para organizar o ambiente. A camada bronze preserva os dados brutos em JSON.

## Decisões e próximos passos
A evolução do projeto envolve estudar ingestão idempotente, captura de mudanças, formatos analíticos abertos e tratamento de reprocessamento. Esses tópicos fazem parte do planejamento e não representam funcionalidades concluídas nesta apresentação.

O código e a documentação do repositório são a referência para acompanhar o estado atual da implementação.
