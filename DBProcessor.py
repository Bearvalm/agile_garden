import sqlite3
import security


class DBProcessor:

	def __init__(self, db_name):
		self._cursor = None
		self._connection = None
		self.connect_to_db(db_name)



	def name_is_not_correct(self, name):
		'''
		Check if provided name is not secure. It is secure if name cosists only of such
		characters as 'a-z', 'A-Z', '0-9', '_'. If it is not secure, returns True.
		If it is secure, returns False.
		'''
		if security.name_is_not_correct(name):
			print('Name is not correct!')
			return True
		return False



	def connect_to_db(self, db_name):
		'''
		Connects to database with name db_name.
		'''
		self._connection = sqlite3.connect(db_name)
		self._cursor = self._connection.cursor()



	def create_table(self, table_name, table_columns):
		'''
		Creates table with name table_name and columns table_columns, provided as iterable.
		'''
		if self.name_is_not_correct(table_name):
			return
		query = 'create table if not exists {0}({1});'.format(table_name, ', '.join(table_columns))
		self._cursor.execute(query)


	def insert_data(self, table_name, data, is_one_row=True):
		'''
		Inserts data in table with name table_name. Data needs to be iterable.
		Argument is_one_row provides the answer to how many rows are being
		inserted in table.
		'''
		if self.name_is_not_correct(table_name):
			return

		if is_one_row:
			columns_number = ', '.join('?' * len(data))
			query = 'insert into {0} values({1})'.format(table_name, columns_number)
			print(query)
			self._cursor.execute(query, data)
		else:
			columns_number = ', '.join('?' * len(data[0]))
			query = 'insert into {0} values({1})'.format(table_name, columns_number)
			self._cursor.executemany(query, data)

		self._connection.commit()


	def update_data(self, table_name, column_names, data, update_by, is_one_row=True):
		'''
		Updates data in table with name table_name. Data needs to be iterable
		as well as column_names that are columns that are being updated.
		Argument update_by provides column and value to identify the row for updating.
		Argument is_one_row provides the answer to how many rows are being
		updated in table.
		'''
		args = table_name, *column_names
		if any([self.name_is_not_correct(arg) for arg in args]):
			return

		columns_number = ', '.join([col + ' = ?' for col in column_names])
		to_update_by = '{0} = ?'.format(update_by[0] if is_one_row else update_by[0][0])
		query = 'update {0} set {1} where {2};'.format(table_name, columns_number, to_update_by)
		if is_one_row:
			update_data = data + (update_by[1],)
			self._cursor.execute(query, update_data)
		else:
			update_data = [data[x] + (update_by[x][1],) for x in range(len(data))]
			self._cursor.executemany(query, update_data)
		self._connection.commit()


	def delete_row(self, table_name, column_name, value):
		'''
		Delete row from table with name table_name. The row is identified by
		the name of the column column_name and the value of this column in the
		row.
		'''
		args = table_name, column_name
		if any([self.name_is_not_correct(arg) for arg in args]):
			return

		query = 'delete from {0} where {1} = ?;'.format(table_name, column_name)
		self._cursor.execute(query, (value,))
		self._connection.commit()


	def drop_table(self, table_name):
		'''
		Delete table from database with the name of table table_name.
		'''
		if self.name_is_not_correct(table_name):
			return
		query = 'drop table if exists {};'.format(table_name)
		self._cursor.execute(query)


	def select_one(self, table_name, select_by):
		'''
		Gets one row from table with the name table_name. The row is
		identified by argument select_by which is the name of the column
		and the value of this column in the row that is needed.
		'''
		column, value = select_by
		args = table_name, column
		if any([self.name_is_not_correct(arg) for arg in args]):
			return
		query = 'select * from {0} where {1} = ?;'.format(table_name, column)
		self._cursor.execute(query, (value,))
		return self._cursor.fetchone()


	def select_custom(self, table_name, select_what, select_by={}):
		args = table_name, *select_what
		if any([self.name_is_not_correct(arg) for arg in args]):
			return

		query = 'select {0} from {1}'.format(','.join(select_what), table_name)

		if select_by:
			query += ' where {0} = ?;'.format(select_by[0])
			self._cursor.execute(query, (select_by[1],))
		else:
			query += ';'
			self._cursor.execute(query)
		return self._cursor.fetchall()


# if __name__ == '__main__':
# 	_connection, _cursor = connect_to_db('test.db')

# 	# query = 'insert into tbl values(?, ?, ?);'
# 	# _cursor.execute(query, ('5', 'sfd', 'sda'))
# 	# _connection.commit()
# 	columns = ('id int', 'word text', 'translation text')
# 	create_table('tbl', columns)
# 	data = [(0, 'access', 'доступ'), (1, 'give', 'давать'),]
# 	insert_data('tbl', data, is_one_row=False)
# 	data_new = [('access', 'дос'), ('give', 'дав')]
# 	cols = ['word', 'translation']
# 	update_by = [('id', 1), ('id', 10)]
# 	update_data('tbl', cols, data_new, update_by, is_one_row=False)
# 	print(select_one('tbl', ['id', 19]))
# 	# delete_row('tbl', 'id', 0)
# 	# drop_table('s_d')
# 	# _cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
# 	# l = _cursor.fetchall()
# 	# print(l)
