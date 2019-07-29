from database import Database

db = Database()

if __name__ == '__main__':
	collection = db.collection('my_collection/doc/other_collection')
	collection.add({ 'num': 0 })
	document = collection.documents[0]
	print(document.get())
	document.update({ 'ken': 5 })
	print(document.get())
	print(document.id)
	print(len(collection.documents))
	print(db)