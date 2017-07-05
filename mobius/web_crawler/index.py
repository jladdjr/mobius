# -*- coding: utf-8 -*-
import os
import sqlite3

class Index(object):

    def __init__(self, database_path=''):
        if not database_path:
            database_path = os.environ.get('MOBIUS_INDEX_DB_PATH', 'mobius.db')
        self._database_path = database_path

    def __enter__(self):
        # print("enter __enter__")
        self._conn = sqlite3.connect(self._database_path)
        self._initialize_tables()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # print("enter __exit__")
        self._conn.close()

    def __repr__(self):
	cur = self._conn.cursor()
	text = u'sites\n-----\n'
        for rowid, address in cur.execute(u'''SELECT rowid, address FROM sites''').fetchall():
            address = (address[:58] + u"..") if len(address) > 60 else address
            address = address.ljust(60)
            text += u"{0} {1}\n".format(rowid, address)
        
        for table in cur.execute(u'''SELECT name FROM sqlite_master WHERE type="table"''').fetchall():
            if table[0] == u'sites':
                continue
	    text += u'\n{0}\n{1}\n'.format(table[0], u'-' * len(table[0]))
	    for site_id, relevance in cur.execute(u'''SELECT site_id, relevance FROM {0}'''.format(table[0])).fetchall():
		text += u"{0} {1}\n".format(str(site_id).ljust(3), relevance)
        return text[:-1]

    __str__ = __repr__

    def _initialize_tables(self):
        # print("enter _initialize_tables")
        cur = self._conn.cursor()
        if not cur.execute(u'''SELECT name FROM sqlite_master WHERE type="table" and name="sites"''').fetchone():
            cur.execute(u'''CREATE TABLE sites (address VARCHAR(255))''')
            # print(" create sites")
            self._conn.commit()

    def reset(self):
        # print("enter reset")
        cur = self._conn.cursor()
        for table in cur.execute(u'''SELECT name FROM sqlite_master WHERE type="table"''').fetchall():
            # print(" drop {}".format(table[0]))
            cur.execute(u'DROP TABLE {}'.format(table[0]))
        self._conn.commit()
        cur = self._conn.cursor()
        cur.execute(u'''CREATE TABLE sites (address VARCHAR(255))''')
        # print(" create sites")
        self._conn.commit()

    def index_site(self, url, weighted_topics):
        # print("enter index_site")
        site_id = self._get_or_create_site(url)
        for topic, relevance in weighted_topics:
            self._add_site_to_topic(site_id, topic, relevance)

    def _get_or_create_site(self, url):
        # print("enter _get_or_create_site")
        cur = self._conn.cursor()
        if not cur.execute(u'''SELECT rowid FROM sites WHERE address=?''', (url,)).fetchone():
            # print("create site {}".format(url))
            cur.execute(u'''INSERT INTO sites (address) VALUES (?)''', (url,))
            self._conn.commit()

        return cur.execute(u'''SELECT rowid FROM sites WHERE address=?''', (url,)).fetchone()[0]

    def _ensure_topic_exists(self, topic):
        topic = unicode(topic.lower())
        # print("enter _ensure_topic_exists")
        cur = self._conn.cursor()
        if not cur.execute(u'''SELECT name FROM sqlite_master WHERE type='table' and name=?''', ('topic_' + topic, )).fetchone():
            # print(" create table {}".format('topic_' + topic))
            cur.execute('''CREATE TABLE {} (site_id INTEGER, relevance INTEGER)'''.format('topic_' + topic))
            self._conn.commit()

    def _add_site_to_topic(self, site_id, topic, relevance):
        topic = unicode(topic.lower())
        # print('enter _add_site_to_topic')
        self._ensure_topic_exists(topic)
        cur = self._conn.cursor()
        # print(' add site to {}'.format('topic_' + topic))
        cur.execute(u'''INSERT INTO {} VALUES (?, ?)'''.format(u'topic_' + topic), (site_id, relevance))
        self._conn.commit()
