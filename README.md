# O Cacaio: Análise Comparativa de Linhagens Celulares CCLE e Tumores Primários

## Aplicação Web
Disponível em: https://caiomussatto.shinyapps.io/

## Descrição do Projeto
O Cacaio é um projeto de mestrado em Bioinformática que realizou análise comparativa entre linhagens celulares da Cancer Cell Line Encyclopedia (CCLE) e tumores primários humanos. O objetivo foi identificar quais linhagens do CCLE apresentam maior similaridade transcriptômica com tumores primários específicos, facilitando a seleção de modelos celulares mais representativos para pesquisa oncológica.

## Conjunto de Dados
Foram analisados 11 datasets de single-cell RNA-seq:

### Tumores Primários (10 tipos)
- Cérebro
- Mama
- Cólon
- Rim
- Pulmão
- Nasofaringe
- Ovário
- Pâncreas
- Próstata
- Pele

### Linhagens Celulares
- Cancer Cell Line Encyclopedia (CCLE)

### Métricas
- Total de células analisadas: 258.370
- Total de genes analisados: 21.792
- Células de tumores primários: ~200.000
- Células de linhagens CCLE: ~58.370

## Pipeline de Análise

### Processamento Individual por Tipo Tumoral
Para cada tipo de câncer, foi seguido o pipeline padrão de análise de single-cell RNA-seq:

1. Controle de qualidade baseado em contagens totais, genes detectados e percentual mitocondrial
2. Normalização logarítmica e identificação de genes altamente variáveis
3. Redução de dimensionalidade via PCA
4. Clusterização utilizando algoritmos de comunidade
5. Anotação de tipos celulares com base em marcadores conhecidos

### Integração Multi-dataset
1. Integração dos 11 datasets utilizando métodos de correção de batch effects
2. Avaliação da qualidade de integração com métricas do pacote ```scib```
3. Análise da preservação de sinal biológico versus remoção de efeitos técnicos

### Análise de Similaridade
1. Cálculo de correlação de distância entre perfis transcriptômicos de tumores primários e linhagens CCLE
2. Construção de matrizes de distância em espaço de componentes principais
3. Geração de rankings de similaridade por tipo tumoral

## Implementação Técnica

### Stack Tecnológico
Todas as análises foram implementadas em Python utilizando os seguintes pacotes:

- ```Scanpy``` e ```AnnData``` para processamento de single-cell RNA-seq
- ```HarmonyPy``` para integração de dados
- ```scikit-learn``` e ```scipy``` para análises estatísticas
- ```scib``` para avaliação da integração
- ```matplotlib``` e ```seaborn``` para visualização
- ```dcor``` para calcular a distância de correlação


### Correlação de Distância
A análise de similaridade foi baseada em correlação de distância, calculando a correlação entre matrizes de distância de tumores primários e linhagens CCLE no espaço transcriptômico integrado.

## Aplicação Web

### Funcionalidades
A aplicação web disponível em https://caiomussatto.shinyapps.io/ oferece:

1. Consulta interativa de rankings de similaridade por tipo de câncer
2. Visualização de perfis de expressão comparativos
3. Download de tabelas de correlação e rankings
4. Documentação metodológica completa

### Público-Alvo
- Pesquisadores em oncologia translacional
- Desenvolvedores de fármacos
- Acadêmicos em ciências biomédicas

## Aplicações Práticas

### Para Pesquisa Translacional
- Seleção informada de modelos celulares para estudos específicos
- Identificação de limitações de linhagens existentes
- Planejamento experimental com maior relevância translacional

### Para Desenvolvimento de Fármacos
- Triagem em modelos mais representativos de tumores primários
- Redução de falhas na transição para ensaios clínicos
- Identificação de modelos para estudos de resistência terapêutica

## Reprodutibilidade
O pipeline completo está implementado em Python e inclui:
- Scripts modulares para cada etapa de análise
- Documentação de parâmetros e versões de pacotes
- Dados processados para validação
- Instruções para replicação dos resultados

## Autoria
**Pesquisador:** Caio Mussatto  
**Orientador:** Robson Franscisco Carvalho 
**Instituição:** Instituto de Biociências de Botucatu  
**Programa:** Ciências Biológicas (Genética)
