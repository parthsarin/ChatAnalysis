#!/usr/bin/env python3
import db
import collections
import pathlib
from datetime import datetime
import pickle

Message = collections.namedtuple('Message', ['text', 'date', 'is_from_me'])

def _search_in_users(keys, filename):
	"""Searches for users with a certain key.

	:keys: A list of strings to search for.
	:filename: The filename of the database.
	"""
	database = db.DB(username='', password='', hostname='', filename=filename, dbtype='sqlite')
	all_people = database.tables.chat.all()
	for person in all_people.itertuples():
		truthtable = [ k in person.guid for k in keys ]
		if any(truthtable): # if any of the keys match
			print(person)

def convert_datetime(num):
	"""Convert Cocoa Datetime objects to Python objects.
	
	:num: The Cocoa datetime as an integer.
	"""
	unix = datetime(1970, 1, 1)  # UTC
	cocoa = datetime(2001, 1, 1)  # UTC

	delta = cocoa - unix  # timedelta instance
	
	return datetime.fromtimestamp(num // 1000000000) + delta

def load_messages_for_id(id):
	"""Load messages for a particular chat id.

	:id: The id of the person with whom messages are shared.
	"""
	saved_data = pathlib.Path(f'.{id}_dat')
	if saved_data.exists():
		with saved_data.open('rb') as f:
			return pickle.load(f)

	return False

def save_messages_for_id(id, messages):
	"""Save messages with a particular chat id.

	:id: The id of person with whom the messages are shared.
	"""
	saved_data = pathlib.Path(f'.{id}_dat')
	with saved_data.open('wb') as f:
		pickle.dump(messages, f)

def clean_messages(dirty_messages):
	"""Cleans message data by converting it to a list of Message
	objects.

	:dirty_messages: Dirty message data.
	"""
	output = []

	for row, message in dirty_messages.iterrows():
		text = message['text']
		date = convert_datetime(int(message['date']))
		from_me = bool(int(message['is_from_me']))

		output.append(Message(text, date, from_me))

	return output

def get_messages_for_id(id, filename):
	"""Returns the messages shared with a person of a particular id
	as a list of Message objects.

	:id: The id of the person with whom the messages are shared.
	:filename: The filename of the database.
	"""
	load = load_messages_for_id(id)
	if load:
		return load

	print("This is the first time you've searched for this user. Loading the database...")
	database = db.DB(username='', password='', hostname='', filename=filename, dbtype='sqlite')

	chat_user = database.tables.chat_message_join.all()
	all_messages = database.tables.message.all()

	message_ids = set()
	for row, chat_data in chat_user.iterrows():
		if chat_data['chat_id'] == id:
			# The message belongs to the user in question
			message_ids.add(chat_data['message_id'])

	dirty_messages = all_messages.loc[all_messages['ROWID'].isin(message_ids)]
	return clean_messages(dirty_messages)
