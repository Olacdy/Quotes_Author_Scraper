# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
import json
import re
import yaml
import xml.etree.ElementTree as ET
import mysql.connector


class JsonWriterPipeline(object):
    def open_spider(self, spider):
        self.file_path = 'QuotesAuthors.json'
        self.file = open(self.file_path, 'w')
        self.file.write('{"authors": [')

    def close_spider(self, spider):
        self.file.write("]}")
        self.file.close()
        data = yaml.load(open(self.file_path))
        with open(self.file_path, 'w') as file:
            file.write(json.dumps(data,
                                  indent=4,
                                  sort_keys=True,
                                  separators=(',', ': ')))

    def process_item(self, item, spider):
        line = json.dumps(
            dict(process_item(item)),
            indent=4,
            sort_keys=True,
            separators=(',', ': ')
        ) + ",\n"
        self.file.write(line)
        return item


class SQLiteWriterPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def close_spider(self, spider):
        self.connection.close()

    def create_connection(self):
        self.connection = sqlite3.connect("QuotesAuthors.db")
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS quotes_author_tb""")
        self.cursor.execute("""CREATE TABLE quotes_author_tb (
                            name TEXT,
                            birth_date DATE,
                            birth_place TEXT,
                            description TEXT
                            )""")

    def process_item(self, item, spider):
        self.store_db(process_item(item))
        return item

    def store_db(self, item):
        self.cursor.execute("""INSERT INTO quotes_author_tb VALUES (?, ?, ?, ?)""",
                            (
                                item['name'],
                                item['birth_date'],
                                item['birth_place'],
                                item['description']
                            ))
        self.connection.commit()


class MySQLWriterPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()

    def close_spider(self, spider):
        self.connection.close()

    def create_connection(self):
        self.connection = mysql.connector.connect(
                        host='localhost',
                        user='root',
                        passwd='password',
                        database='my_authors'
        )
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS quotes_author_tb""")
        self.cursor.execute("""CREATE TABLE quotes_author_tb (
                            name TEXT,
                            birth_date TEXT,
                            birth_place TEXT,
                            description TEXT
                            )""")

    def process_item(self, item, spider):
        self.store_db(process_item(item))
        return item

    def store_db(self, item):
        self.cursor.execute("""INSERT INTO quotes_author_tb VALUES (%s, %s, %s, %s)""",
                            (
                                item['name'],
                                item['birth_date'],
                                item['birth_place'],
                                item['description']
                            ))
        self.connection.commit()


class XMLWriterPipeline(object):

    def __init__(self):
        self.authors = ET.Element('authors')
        self.file_path = "QuotesAuthors.xml"

    def open_spider(self, spider):
        self.file = open(self.file_path, "wb")
        pass

    def close_spider(self, spider):
        authors_data = ET.tostring(self.authors)
        self.file = open(self.file_path, "wb")
        self.file.write(authors_data)
        pass

    def process_item(self, item, spider):
        item = process_item(item)
        author = ET.SubElement(self.authors, 'author')
        author_birth_date = ET.SubElement(author, 'a_birth_date')
        author_birth_place = ET.SubElement(author, 'a_birth_place')
        author_description = ET.SubElement(author, 'a_description')
        author.set('name', item['name'])
        author_birth_date.text = item['birth_date']
        author_birth_place.text = item['birth_place']
        author_description.text = item['description']
        return item


def process_item(item):
    for k in item.fields:
        item[k] = str(item[k][0]).strip()
    item['birth_place'] = re.sub('in ', '', item['birth_place'])
    return item
