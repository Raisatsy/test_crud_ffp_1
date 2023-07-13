from pyArango.connection import Connection

"""У меня коллекция в Arango DB создается сама при первом получении данных"""

def connect_to_db():
    conn = Connection(
        arangoURL='http://localhost:8529'
    )
    db = conn['test']
    return db
