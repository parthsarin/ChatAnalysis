#!/usr/bin/env python3
from utils import Message
import collections
import emoji
import re

MOST_COMMON_WORDS = {"i'm", 'are', "don't", "it's", 'a', 'about', 'after', 'all', 'also', 'an', 'and', 'any', 'as', 'at', 'back', 'be', 'because', 'but', 'by', 'can', 'come', 'could', 'day', 'do', 'even', 'first', 'for', 'from', 'get', 'give', 'go', 'good', 'have', 'he', 'her', 'him', 'his', 'how', 'i', 'if', 'in', 'is', 'into', 'it', 'its', 'just', 'know', 'like', 'look', 'make', 'me', 'most', 'my', 'new', 'no', 'not', 'now', 'of', 'on', 'one', 'only', 'or', 'other', 'our', 'out', 'over', 'people', 'say', 'see', 'she', 'so', 'some', 'take', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'think', 'this', 'time', 'to', 'two', 'up', 'us', 'use', 'want', 'way', 'we', 'well', 'what', 'when', 'which', 'who', 'will', 'with', 'work', 'would', 'year', 'you', 'your'}

def analyze_sender_frequency(messages):
	"""Analyzes who is more frequently the sender and who
	is more frequently the reciever.

	:returns: A pair of ints ( messages_from_other, messages_from_parth )
	"""
	messages_from_parth = len([ message for message in messages if message.is_from_me ])
	messages_from_other = len(messages) - messages_from_parth

	return messages_from_other, messages_from_parth

def clean_message(message):
	"""Cleans a message string so that it can be properly
	counted.

	:message: A string containing the text from one message.
	"""
	message = message.lower()
	
	# Regex cleaning
	REPLACE_NO_SPACE = re.compile("[.;:’!\'?,\"()\[\]]")
	REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

	message = REPLACE_NO_SPACE.sub("", message)
	message = REPLACE_WITH_SPACE.sub(" ", message)

	message = message.split() # split by whitespace
	message = filter(lambda word: word not in MOST_COMMON_WORDS, message) # remove common words

	return list(message)

def analyze_word_frequency(messages):
	"""Analyzes the word frequency of the message data.

	:returns: A pair of counter objects ( words_by_other, words_by_parth )
	"""
	d = collections.defaultdict(collections.Counter)

	for message in messages:
		if message.text:
			words = clean_message(message.text)
			for word in words:
				if message.is_from_me:
					d['parth'][word.strip()] += 1
				else:
					d['other'][word.strip()] += 1

	return d['other'], d['parth']

def analyze_emoji_frequency(messages):
	"""Analyzes the emoji frequency of the message data.

	:returns: A pair of counter objects ( emojis_by_other, emojis_by_parth )
	"""
	d = collections.defaultdict(collections.Counter)

	for message in messages:
		if message.text:
			emojis = [ ch for ch in message.text if ch in emoji.UNICODE_EMOJI ]
			for e in emojis:
				if message.is_from_me:
					d['parth'][e] += 1
				else:
					d['other'][e] += 1

	return d['other'], d['parth']

def analyze_length(messages):
	"""Analyzes the length of messages as lists of words and characters.

	:returns: A pair of AverageLength objects ( avg_len_other, avg_len_parth )
	"""
	AverageLength = collections.namedtuple('AverageLength', ['words', 'chars'], defaults=[0, 0])

	# Counter variables
	avg_len = [ [0, 0], [0, 0] ] # other [ words, chars ], parth [ words, chars ]
	total_chars = [ 0, 0 ]
	total_words = [ 0, 0 ]

	# Count all chars and words
	for message in messages:
		index = 1 if message.is_from_me else 0
		if message.text:
			avg_len[index][1] += len(message.text)
			total_chars[index] += 1

			words = clean_message(message.text)
			if words:
				avg_len[index][0] += len(words)
				total_words[index] += 1

	# Normalize for the averages
	output = []
	for i in range(2):
		if total_chars[i]:
			chars = avg_len[i][1] / total_chars[i]
		else:
			chars = avg_len[i][1]

		if total_words[i]:
			words = avg_len[i][0] / total_words[i]
		else:
			words = avg_len[i][0]

		output.append(AverageLength(round(words, 2), round(chars, 2)))

	return output