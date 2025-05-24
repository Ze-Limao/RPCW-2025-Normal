from rdflib import Graph, Namespace, RDF, OWL, Literal, URIRef, XSD
import json

g = Graph()
g.parse("sapientia_base.ttl")
n = Namespace("http://www.semanticweb.org/jeswi/ontologies/2025/untitled-ontology-39#")


disciplinas = set()
conceitos_set = set()
periodo_historico = set()
aplicacoes = set()
conhecimentos = set()
mestres = set()


# Processa dados dos alunos
with open("pg55967.json", "r") as f:
    data = json.load(f)

for i, aluno in enumerate(data):
    nome = aluno["nome"].replace(' ', '_')
    idade = aluno["idade"]
    id_ = f"{nome}_{i}"

    aluno_uri = n[id_]
    g.add((aluno_uri, RDF.type, OWL.NamedIndividual))
    g.add((aluno_uri, RDF.type, n.Aluno))

    g.add((aluno_uri, n.idAluno, Literal(id_)))
    g.add((aluno_uri, n.nome, Literal(nome)))
    g.add((aluno_uri, n.idade, Literal(idade, datatype=XSD.int)))

    for disciplina in aluno["disciplinas"]:
        disc_id = disciplina.replace(' ', '_')
        disc_uri = n[disc_id]

        if disc_id not in disciplinas:
            g.add((disc_uri, RDF.type, OWL.NamedIndividual))
            g.add((disc_uri, RDF.type, n.Disciplina))
            disciplinas.add(disc_id)

        g.add((aluno_uri, n.aprende, disc_uri))


# Processa conceitos
with open("conceitos.json", "r") as file:
    conceitos = json.load(file)["conceitos"]

    for conceito in conceitos:
        conceito_uri = n[conceito["nome"].replace(" ", "_")]
        if conceito_uri not in conceitos_set:
            g.add((conceito_uri, RDF.type, n.Conceito))
            conceitos_set.add(conceito_uri)

        g.add((conceito_uri, n.nome, Literal(conceito["nome"], datatype=XSD.string)))

        for aplicacao in conceito["aplicações"]:
            aplicacao_uri = n[aplicacao.replace(" ", "_")]
            if aplicacao_uri not in aplicacoes:
                g.add((aplicacao_uri, RDF.type, n.Aplicacao))
                g.add((aplicacao_uri, n.nome, Literal(aplicacao, datatype=XSD.string)))
                aplicacoes.add(aplicacao_uri)
            g.add((conceito_uri, n.temAplicacaoEm, aplicacao_uri))

        periodo = conceito["períodoHistórico"]
        periodo_uri = n[periodo.replace(" ", "_")]
        if periodo_uri not in periodo_historico:
            g.add((periodo_uri, RDF.type, n.PeriodoHistorico))
            g.add((periodo_uri, n.nome, Literal(periodo, datatype=XSD.string)))
            periodo_historico.add(periodo_uri)
        g.add((conceito_uri, n.surgeEm, periodo_uri))

        for conceito_relacionado in conceito["conceitosRelacionados"]:
            conceito_relacionado_uri = n[conceito_relacionado.replace(" ", "_")]
            if conceito_relacionado_uri not in conceitos_set:
                g.add((conceito_relacionado_uri, RDF.type, n.Conceito))
                conceitos_set.add(conceito_relacionado_uri)
            g.add((conceito_uri, n.temConceitoRelacionado, conceito_relacionado_uri))


# Processa disciplinas
with open("disciplinas.json", "r") as file:
    disciplinas_data = json.load(file)["disciplinas"]

    for disciplina in disciplinas_data:
        disciplina_uri = n[disciplina["nome"].replace(" ", "_")]
        if disciplina_uri not in disciplinas:
            g.add((disciplina_uri, RDF.type, n.Disciplina))
            disciplinas.add(disciplina_uri)

        g.add((disciplina_uri, n.nome, Literal(disciplina["nome"], datatype=XSD.string)))

        for conhecimento in disciplina["tiposDeConhecimento"]:
            conhecimento_uri = n[conhecimento.replace(" ", "_")]
            if conhecimento_uri not in conhecimentos:
                g.add((conhecimento_uri, RDF.type, n.TipoDeConhecimento))
                g.add((conhecimento_uri, n.nome, Literal(conhecimento, datatype=XSD.string)))
                conhecimentos.add(conhecimento_uri)
            g.add((disciplina_uri, n.pertenceA, conhecimento_uri))

        if "conceitos" in disciplina:
            for conceito in disciplina["conceitos"]:
                conceito_uri = n[conceito.replace(" ", "_")]
                if conceito_uri not in conceitos_set:
                    g.add((conceito_uri, RDF.type, n.Conceito))
                    conceitos_set.add(conceito_uri)
                g.add((conceito_uri, n.eEstudadoEm, disciplina_uri))


# Processa mestres
with open("mestres.json", "r") as file:
    mestres_data = json.load(file)["mestres"]

    for mestre in mestres_data:
        mestre_uri = n[mestre["nome"].replace(" ", "_")]
        g.add((mestre_uri, RDF.type, n.Mestre))
        g.add((mestre_uri, n.nome, Literal(mestre["nome"], datatype=XSD.string)))
        mestres.add(mestre_uri)

        periodo_uri = n[mestre["períodoHistórico"].replace(" ", "_")]
        if periodo_uri not in periodo_historico:
            g.add((periodo_uri, RDF.type, n.PeriodoHistorico))
            g.add((periodo_uri, n.nome, Literal(mestre["períodoHistórico"], datatype=XSD.string)))
            periodo_historico.add(periodo_uri)
        g.add((mestre_uri, n.viveuEm, periodo_uri))

        for disciplina in mestre["disciplinas"]:
            disciplina_uri = n[disciplina.replace(" ", "_")]
            if disciplina_uri not in disciplinas:
                g.add((disciplina_uri, RDF.type, n.Disciplina))
                disciplinas.add(disciplina_uri)
            g.add((mestre_uri, n.ensina, disciplina_uri))


# Processa obras
with open("obras.json", "r") as file:
    obras_data = json.load(file)["obras"]

    for obra in obras_data:
        obra_uri = n[obra["titulo"].replace(" ", "_")]
        g.add((obra_uri, RDF.type, n.Obra))

        autor_uri = n[obra["autor"].replace(" ", "_")]
        if autor_uri not in mestres:
            g.add((autor_uri, RDF.type, n.Mestre))
            g.add((autor_uri, n.nome, Literal(obra["autor"], datatype=XSD.string)))
            mestres.add(autor_uri)

        g.add((obra_uri, n.titulo, Literal(obra["titulo"], datatype=XSD.string)))
        g.add((obra_uri, n.foiEscritoPor, autor_uri))

        for conceito in obra["conceitos"]:
            conceito_uri = n[conceito.replace(" ", "_")]
            if conceito_uri not in conceitos_set:
                g.add((conceito_uri, RDF.type, n.Conceito))
                conceitos_set.add(conceito_uri)
            g.add((obra_uri, n.explica, conceito_uri))


# Serializa para ficheiro Turtle e imprime informação de resumo
print(g.serialize("sapientia_ind.ttl", format="turtle"))
print("Total de triplas no grafo:", len(g))
