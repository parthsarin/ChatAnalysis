#!/usr/bin/env python3

def print_num(person1, person2):
	"""Prettily print the number of some category that each
	person has sent to the other.

	:type person1: ( str, int )
	"""
	print(f"{person1[0].title()}: {person1[1]}")
	print(f"{person2[0].title()}: {person2[1]}")

def print_most_common(person1, person2, n):
	"""Prettily print the n most common exchanges
	that the two people have had, indexed in the counter.

	:type person1: ( str, collections.Counter )
	:type n: int
	"""
	print(f"{ person1[0].title() }")
	print("-"*20)
	for i, indexed_attr in enumerate(person1[1].most_common(n)):
		print(f"{i+1}. {indexed_attr[0]} ({indexed_attr[1]} times)")

	print()

	print(f"{ person2[0].title() }")
	print("-"*20)
	for i, indexed_attr in enumerate(person2[1].most_common(n)):
		print(f"{i+1}. {indexed_attr[0]} ({indexed_attr[1]} times)")