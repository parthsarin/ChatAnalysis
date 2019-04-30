#!/usr/bin/env python3
import sys
import db
import collections
import pathlib
from datetime import datetime
import pickle
import emoji

from utils import Message
import utils
import analysisutils as au
import ioutils

from config import PEOPLE

def analyze_person(k, filename):
	person_id = PEOPLE[k].ids

	# Get message data
	if isinstance(person_id, list):
		main_id = person_id[0]
		messages = utils.load_messages_for_id(main_id)

		if not messages:
			messages = []

			for user_id in person_id:
				messages += utils.get_messages_for_id(user_id, filename)

			utils.save_messages_for_id(main_id, messages)
	else:
		messages = utils.get_messages_for_id(person_id, filename)
		utils.save_messages_for_id(person_id, messages)


	# Analyze data
	messages_from_other, messages_from_parth = au.analyze_sender_frequency(messages)
	other_words, parth_words = au.analyze_word_frequency(messages)
	emojis_from_other, emojis_from_parth = au.analyze_emoji_frequency(messages)

	# Print data
	print("Number of messages:")
	ioutils.print_num_messages((PEOPLE[k].name, messages_from_other), ('Parth', messages_from_parth))

	print()

	print("Most common words:")
	ioutils.print_most_common((PEOPLE[k].name, other_words), ('Parth', parth_words), 20)

	print()

	print("Most common emojis:")
	ioutils.print_most_common((PEOPLE[k].name, emojis_from_other), ("Parth", emojis_from_parth), 20)

def main():
	to_analyze = sys.argv[1:]
	for person in to_analyze:
		if person.lower() in PEOPLE:
			analyze_person(person.lower(), 'chat.db')


if __name__ == '__main__':
	main()
