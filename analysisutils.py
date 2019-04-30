#!/usr/bin/env python3
from utils import Message
import collections
import emoji

MOST_COMMON_WORDS = {"i'm", 'are', "don't", "it's", 'a', 'about', 'after', 'all', 'also', 'an', 'and', 'any', 'as', 'at', 'back', 'be', 'because', 'but', 'by', 'can', 'come', 'could', 'day', 'do', 'even', 'first', 'for', 'from', 'get', 'give', 'go', 'good', 'have', 'he', 'her', 'him', 'his', 'how', 'i', 'if', 'in', 'is', 'into', 'it', 'its', 'just', 'know', 'like', 'look', 'make', 'me', 'most', 'my', 'new', 'no', 'not', 'now', 'of', 'on', 'one', 'only', 'or', 'other', 'our', 'out', 'over', 'people', 'say', 'see', 'she', 'so', 'some', 'take', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'think', 'this', 'time', 'to', 'two', 'up', 'us', 'use', 'want', 'way', 'we', 'well', 'what', 'when', 'which', 'who', 'will', 'with', 'work', 'would', 'year', 'you', 'your'}

def analyze_sender_frequency(messages):
	"""Analyzes who is more frequently the sender and who
	is more frequently the reciever.

	:returns: A pair of ints ( messages_from_other, messages_from_parth )
	"""
	messages_from_parth = len([ message for message in messages if message.is_from_me ])
	messages_from_other = len(messages) - messages_from_parth

	return messages_from_other, messages_from_parth

def analyze_word_frequency(messages):
	"""Analyzes the word frequency of the message data.

	:returns: A pair of counter objects ( words_by_other, words_by_parth )
	"""
	d = collections.defaultdict(collections.Counter)

	for message in messages:
		if message.text:
			words = message.text.lower().split(' ')
			words = filter(lambda word: word not in MOST_COMMON_WORDS, words)
			for word in words:
				if word.strip(): # make sure there's content
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