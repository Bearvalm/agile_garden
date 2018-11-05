import random
from DBProcessor import DBProcessor


PREV_CHOICE = []


def add_word(db, word, translation, language_id, relevance=1):

	data = [None, language_id, word, translation, relevance]
	db.insert_data('Word', data)

	# insert_query = '''insert into Word(word_id, language_id, word, translation, relevance)
	# 					values({0}, {1}, {2}, {3}, {4})
	# 				'''.format(word_id, language_id, word, translation, relevance)


def add_words(db, words, sep='-'):
	for text in words:
		word, translation = text.split(sep)
		add_word(db, word.strip(), translation.strip(), 0)


def init_db():
	database_name = 'test.db'

	db = DBProcessor(database_name)

	language_columns = ['language_id integer primary key',
	                    'name text not null']

	word_columns = ['word_id integer primary key',
	                'language_id integer not null',
	                'word text not null',
	                'translation text not null',
	                'relevance real not null',
	                'foreign key(language_id) references Language(language_id)']

	user_learned_columns = ['user_id integer not null',
	                        'word_id integer not null',
	                        'times_shown integer not null',
	                        'foreign key(word_id) references Word(word_id)']

	db.create_table('Language', language_columns)
	db.create_table('Word', word_columns)
	db.create_table('UserLearned', user_learned_columns)
	return db


def get_word(db):
	indexes = get_indexes_of_words(db)
	global PREV_CHOICE

	current_choice = random.choice(indexes)
	while current_choice in PREV_CHOICE:
		current_choice = random.choice(indexes)

	if len(PREV_CHOICE) > 3:
		PREV_CHOICE.append()
		PREV_CHOICE = PREV_CHOICE[1:]

	word = db.select_one('Word', {'word_id', current_choice[0]})
	return word


def get_indexes_of_words(db):
	select_what = {'word_id'}
	indexes = db.select_custom('Word', select_what)
	return indexes

#
#
# def read_words(language):
# 	with open('./{}_words'.format(language), 'r') as file:
# 		data = file.read().split('\n')
#
# 	words = {}
# 	for line in data:
# 		word, translation = line.split(' -- ')
# 		words[word] = translation
#
# 	return words
