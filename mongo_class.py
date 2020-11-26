import pymongo
import ssl

class Mongo_db:

    def __init__(self, user, pwd,
                 table="NLP_performance"):
        self.user = user
        client = pymongo.MongoClient(
                "mongodb+srv://" + user + ":" + pwd +
                "@cluster0.x2yjr.gcp.mongodb.net/" + table +
                "?retryWrites=true&w=majority",
                ssl_cert_reqs=ssl.CERT_NONE)
        self.db = client.NLP_performance

    def get_persons(self):
        persons = []
        short = []
        for document in self.db.Person.find():
            persons.append(document["Name"])
            short.append(document["Short"])
        return persons, short

    def get_sentences(self):
        sentences = []
        for document in self.db.Sentences.find():
            sentences.append(document["Sentences"])
        return sentences

    def get_Text(self):
        text = []
        for document in self.db.Text.find():
            text.append(document)
        return text

    def insert_Test_1(self, data):
        data = dict(data)
        self.db.Test_1.insert_one(data)

    def insert_Test_2(self, data):
        data = dict(data)
        self.db.Test_2.insert_one(data)