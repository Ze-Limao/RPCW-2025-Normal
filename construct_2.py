import requests

# Configurações
GRAPHDB_URL = "http://localhost:7200"
REPOSITORY = "sapientia"
QUERY_ENDPOINT = f"{GRAPHDB_URL}/repositories/{REPOSITORY}"
UPDATE_ENDPOINT = f"{GRAPHDB_URL}/repositories/{REPOSITORY}/statements"

HEADERS_QUERY = {
    "Accept": "text/turtle"
}

HEADERS_UPDATE = {
    "Content-Type": "application/sparql-update"
}

# Query CONSTRUCT que cria ligações diretas entre Braga e cidades alcançáveis
construct_query = """
PREFIX : <http://www.semanticweb.org/jeswi/ontologies/2025/untitled-ontology-39#>

CONSTRUCT {
  ?disciplina :daBasesPara ?aplicacao .
}
WHERE {
  ?disciplina :eEstudadoEm ?conceito .
  ?conceito :temAplicacaoEm ?aplicacao .
}
"""

def executar_construct():
    print("Executando CONSTRUCT para obter novos triplos...")
    response = requests.get(QUERY_ENDPOINT, params={"query": construct_query}, headers=HEADERS_QUERY)
    response.raise_for_status()
    return response.text 

def inserir_triplos(triplos_turtle):
    insert_query = f"""
    INSERT DATA {{
      {triplos_turtle}
    }}
    """
    print("Enviando INSERT DATA para aumentar a ontologia...")
    response = requests.post(UPDATE_ENDPOINT, data=insert_query, headers=HEADERS_UPDATE)
    response.raise_for_status()
    print("Inserção concluída com sucesso.")

def main():
    try:
        triplos = executar_construct()
        inserir_triplos(triplos)
    except requests.HTTPError as e:
        print(f"Erro HTTP: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
