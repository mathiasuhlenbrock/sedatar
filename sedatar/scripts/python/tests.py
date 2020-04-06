from sedatar.models import Search

search = Search()


def test_question(question, answer):
    search.question = question
    print(question + ': ' + answer)
    assert search.answer[-1] == answer


print('Testing...')
try:
    test_question('What is a planet?', 'An astronomical object.')
    test_question('What is an exoplanet?', 'A planet.')
    test_question('What is a terrestrial planet?', 'A planet.')
    test_question('What is Jupiter?', 'A gas giant.')
    test_question('What is Kepler-11?', 'A planetary system.')
    test_question('What is Kepler-11 b?', 'A gas giant.')
    test_question('What is the size of Kepler-11?', '0.466 AU.')
    test_question('What is the size of Kepler-11 b?', '0.161 R<sub>♃</sub>.')
    test_question('How many planets are there?', '4149.')
    test_question('How many exoplanets are there?', '4141.')
    test_question('What is the number of planets?', 'Query not generated.')
    test_question('What is an animal?', 'No answer found.')
except AssertionError:
    print('ERROR: Test failed.')
print('Tests complete.')