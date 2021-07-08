from sedatar.models import Search

search = Search()


def test_question(question, answer):
    search.question = question
    print('Q: ' + question)
    print('A: ' + search.answer[-1])
    # print('Q: Expected answer: ' + answer)
    assert search.answer[-1] == answer
    print('Q: Correct!')


print('Begin tests...')
try:
    test_question('What is a planet?', 'An astronomical object.')
    test_question('What is an exoplanet?', 'A planet.')
    test_question('What is a terrestrial planet?', 'A planet.')
    test_question('What is Jupiter?', 'A gas giant.')
    test_question('What is Kepler-11?', 'A planetary system.')
    test_question('What is Kepler-11 b?', 'A gas giant.')
    test_question('What is the size of Kepler-11?', '0.466 AU.')
    test_question('What is the size of Kepler-11 b?', '0.161 R<sub>♃</sub>.')
    test_question('What is the size of a planet?', '0.383 R<sub>♃</sub>.')
    test_question('What is the size of a planetary system?', '12.598 AU.')
    test_question('What is the biggest gas giant?', 'HAT-P-67 b.')
    test_question('What is the smallest gas giant?', 'Kepler-128 b.')
    test_question('What is the largest planet?', 'HD 100546 b.')
    test_question('What is the smallest planet?', 'Kepler-37 b.')
    test_question('What is the biggest terrestrial planet?', 'HD 95338 b.')
    test_question('What is the smallest terrestrial planet?', 'Mercury.')
    test_question('What is the biggest planetary system?', 'USco1556 A.')
    test_question('What is the smallest planetary system?', 'PSR J1719-1438.')
    test_question('What is the closest gas giant?', 'Jupiter.')
    test_question('What is the farthest gas giant?', 'WTS-1 b.')
    test_question('What is the closest planet?', 'Mercury.')
    test_question('What is the farthest planet?', 'OGLE-2015-BLG-0051L b.')
    test_question('What is the closest terrestrial planet?', 'Mercury.')
    test_question('What is the farthest terrestrial planet?', 'PSR J1719-1438 b.')
    test_question('What is the closest planetary system?', 'Proxima Cen.')
    test_question('What is the farthest planetary system?', 'OGLE-2015-BLG-0051L.')
    test_question('How many planets are there?', '4432.')
    test_question('How many exoplanets are there?', '4424.')
    test_question('What is the number of planets?', 'Query not generated.')
    test_question('What is an animal?', 'No answer found.')
    print('Tests complete.')
except AssertionError:
    print('Q: Incorrect!')
    print('Tests failed.')
