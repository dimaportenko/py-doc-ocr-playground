import spacy
from spacy.tokens import DocBin
import pickle


nlp = spacy.blank("en")
print(nlp)

# Load data from pickle file
training_data = pickle.load(open("./data/TrainData.pickle", "rb"))
test_data = pickle.load(open("./data/TestData.pickle", "rb"))

# print(training_data)

# the DocBin will store the example documents
db = DocBin()
for text, annotations in training_data:
    print('-- start text --')
    print(text)
    print('-- end text --')

    doc = nlp(text)
    
    print('-- start doc --')
    print(doc)
    print('-- end doc --')
    ents = []
    for start, end, label in annotations['entities']:
        print(start, end, label)
        span = doc.char_span(start, end, label=label)
        print(span)
        ents.append(span)
    print(ents)
    doc.ents = ents
    db.add(doc)
db.to_disk("./data/train.spacy")


db_test = DocBin()
for text, annotations in test_data:
    doc = nlp(text)
    ents = []
    for start, end, label in annotations['entities']:
        span = doc.char_span(start, end, label=label)
        ents.append(span)
    doc.ents = ents
    db_test.add(doc)
db_test.to_disk("./data/test.spacy")

