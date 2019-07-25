import nltk 
import quepy
import rdflib

if __name__ == '__main__':
    question = 'What is a terrestrial planet?'
    tokens = nltk.wordpunct_tokenize(question)
    print(tokens)
    tags = nltk.pos_tag(tokens)
    print(tags)
    g = rdflib.Graph()
    g.parse('astronomical_database/data/rdf/astronomical_database.rdf')
    sparqlgen = quepy.install('sparqlgen')
    target, query, metadata = sparqlgen.get_query(question)
    if query:
        results = g.query(query)
        if results:
            for result in results:
                print(result)
        else:
            print('No answer found.')
    else:
        print('Query not generated.')
