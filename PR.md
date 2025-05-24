## Ontologia
A ontologia base foi criada no Protege e depois guardade em 'sapientia_base.ttl'

### Povoamento
Utilizei o script de povoamento 'populate.py' que percorre cada um dos json, o povoado ficou no ficheiro 'sapientia_ind.ttl'

## SPARQL
As queries 12 à 23 estao em 'queries.txt'

## Constructs
Criei scripts individuais construct_1 (questão 24 e 25) e construct 2 (questão 26 e 27), que usam uma query SPARQL CONSTRUCT para gerar novos triplos e depois insere esses triplos no repositório local do GraphDB (sapientia).

Os resultados intermedios foram guardados em 'sapientia_ind_estudaCom' e  'sapientia_ind_daBasesPara'
