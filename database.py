from random import random
from exceptions import *

class Database:
	def __init__(self, random_id_length = 20):
		self.collections = []
		self.documents = []
		self.random_id_length = random_id_length

	def __str__(self):
		acc = []
		for collection in self.collections:
			acc.append('-' * len(collection.path.split('/')) + f' {collection.id} (collection)')
			for document in collection.documents:
				acc.append('-' * len(document.path.split('/')) + f' {document.id} (document)')
		return '\n'.join(acc) if len(acc) else '(empty)'

	def collection(self, path):
		segments = list(filter(len, path.split('/')))
		segments_length = len(segments)
		if segments_length == 0 or segments_length % 2 == 0:
			print('Invalid collection path segment count. The segment count must be odd')
			raise InvalidCollectionPath
		for collection in self.collections:
			if collection.path == path:
				return collection
		collection = Database.Collection(self, path)
		self.collections.append(collection)
		return collection
	
	def document(self, path, data = None):
		segments = list(filter(len, path.split('/')))
		segments_length = len(segments)
		if segments_length == 0 or segments_length % 2 == 1:
			print('Invalid document path segment count. The segment count must be even')
			raise InvalidDocumentPath
		for document in self.documents:
			if document.path == path:
				return document
		document = Database.Document(self, path, data)
		self.documents.append(document)
		return document

	class Collection:		
		def __init__(self, database, path):
			self.database = database
			self.id = path.split('/')[-1]
			self.path = path
			self.documents = []
		
		def document(self, path, data = None):
			document = self.database.document(f'{self.path}/{path}', data)
			self.documents.append(document)
			return document
		
		def add(self, data):
			string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
			string_length = len(string)
			return self.document(''.join([string[int(random() * string_length)] for _ in range(self.database.random_id_length)]), data)
	
	class Document:
		def __init__(self, database, path, data = None):
			self.database = database
			self.id = path.split('/')[-1]
			self.path = path
			self.data = data

		def collection(self, path):
			return self.database.collection(f'{self.path}/{path}')

		def get(self):
			return self.data

		def set(self, data):
			self.data = data
			return self
		
		def update(self, data):
			if data is None:
				return self
			if self.data is None:
				self.data = {}
			for key, value in data.items():
				self.data[key] = value
			return self