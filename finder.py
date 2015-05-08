# collection sms spam & ham
# Written by Luavis

import re
import sqlite3

conn = sqlite3.connect('save.db')

def replace_mark(str):
  return re.sub('[\.|\,|"\'|;|:|\?|\||~|`|!|@|#|$|%|^|&|*|(|)|\_|-\|+|\=|\{|\}|\[|\]|\<|\>]+',' ', str)


def load_txt_and_save():
  txt = open("SMSSpamCollection.txt").read()

  spam_word = dict()
  ham_word = dict()

  index = 0;

  for line in txt.split("\r\n"):
    index += 1
    line_split = line.split("\t")
    
    if not len(line_split) == 2:
      print("Pass Index " + str(index) + "\n")
      continue

    line_type = line_split[0]
    target = None

    if line_type == 'spam':
     target = spam_word 
    elif line_type ==  'ham':
      target = ham_word
    else:
      continue

    for c in re.split('\s+', replace_mark(line_split[1])):
      if not len(c) == 0:
        if target.get(c) == None:
          target[c] = 1
        else:
          target[c] += 1;
  
  c = conn.cursor()

  for word in ham_word:
    count = ham_word[word]
    c.execute("insert into ham_word (word, word_count) values('" + word + "', " + str(count) + ")");

  for word in spam_word:
    count = spam_word[word]
    c.execute("insert into spam_word (word, word_count) values('" + word + "', " + str(count) + ")");

  conn.commit()

def write_db():
  c = conn.cursor()

  spam_word_list = open("spam_word.txt", "w+")
  spam_c = c.execute("select * from spam_word order by word_count desc")

  for s in spam_c:
    spam_word_list.write((s[1] + u"\t" + unicode(s[2]) + u"\n").encode('utf8'))

  spam_word_list.close()

  ham_word_list = open("ham_word.txt", "w+")
  ham_c = c.execute("select * from ham_word order by word_count desc")

  for s in ham_c:
    ham_word_list.write((s[1] + u"\t" + unicode(s[2]) + u"\n").encode('utf8'))

  ham_word_list.close()


write_db()

conn.close()

