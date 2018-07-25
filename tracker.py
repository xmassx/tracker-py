from datetime import datetime
from time import sleep
from pprint import pprint
import time
import sqlite3


class abstract_activity(object):
  """
  generate action object
  """
  
  def __init__(self, short, curr_a=None):
    self.short = short
    self.type = self.short_to_type()
    self.id = self.get_id()
    self.name = self.get_name()
    self.status = 'stop'
    self.current_active = curr_a
  
  def short_to_type(self):
    property_dict = {'c': 'context', 'a': 'activity'}
    return property_dict[self.short]
  
  def get_id(self):
    if self.short == 'a':
      return 1
    else:
      return 2
  
  def get_name(self):
    if self.short == 'a':
      return "Programming"
    else:
      return "Home"
  
  def start_activity(self):
    if self.status == 'stop':
      # print("started", self.id)
      self.status = 'run'
      self.current_active.update(self)
    else:
      # print("already start", self.id)
      pass
  
  def stop_activity(self):
    if self.status == 'run':
      # print('stopped', self.id)
      self.status = 'stop'
      self.current_active.update(self)
    else:
      # print('already stopped', self.id)
      pass

class current_activity(object):
  """
  activity with time period in mind
  """
  
  def __init__(self, activity=None, dbo=None):
    # print("init current active")
    if activity:
      self.activity = activity
      self.started = self.get_time()
      self.stopped = ''
      self.write_start_to_dbo()
    else:
      self.activity = None
      self.started = ''
      self.stopped = ''
    if dbo:
      self.dbo = dbo
  
  def get_time(self):
    # a=time.time()
    # return datetime.utcfromtimestamp(a)
    return time.time()
  
  def update(self, activity):
    current_date = self.get_time()
    if self.activity and self.activity.status == 'run':
      self.stopped = current_date
      self.activity.status = 'stop'
      self.write_stop_to_dbo()
    
    self.activity = activity
    self.started = current_date
    self.write_start_to_dbo()
  
  def write_start_to_dbo(self):
    # curr_dict = {'id': self.activity.id, 'state': self.activity.status, 'date': self.started}
    # self.dbo.append(curr_dict)
    curr_tuple = (self.activity.id, self.activity.status, self.started)
    self.dbo.append_tuple(curr_tuple)
  
  def write_stop_to_dbo(self):
    # curr_dict = {'id': self.activity.id, 'state': self.activity.status, 'date': self.stopped}
    # self.dbo.append(curr_dict)
    curr_tuple = (self.activity.id, self.activity.status, self.stopped)
    self.dbo.append_tuple(curr_tuple)


class DBO(object):
  """
  abstract over database
  """
  
  def __init__(self, dbs=':memory:'):
    try:
      create_db = """CREATE TABLE tracker(n INTEGER PRIMARY KEY AUTOINCREMENT,
      id INTEGER, state TEXT, date REAL)"""
      self.INSERT_TEMPLATE = 'INSERT INTO tracker(id, state, date) VALUES(?, ?, ?)'
      self.db = sqlite3.connect(dbs)
      self.cursor = self.db.cursor()
      self.cursor.execute(create_db)
      self.db.commit()
    except Exception as e:
      print(e)
    # self.db = []
  
  def append(self, d={}):
    self.db.append(d)
  
  def append_tuple(self, d=tuple):
    try:
      # print('Hi i have {}'.format(d))
      self.cursor.execute(self.INSERT_TEMPLATE, d)
      self.db.commit()
    except Exception as e:
      print(e)
  
  def print(self):
    try:
      self.cursor.execute('SELECT n, id, state, date FROM tracker')
      fetched = self.cursor.fetchall()
      for row in fetched:
        print(row)
    except Exception as e:
      print(e)
    return None
    


def main():
  # db_file = ':memory:'
  db_file = 'test.sqlite'
  db = DBO(db_file)
  curr_activ = current_activity(None, dbo=db)
  a1 = abstract_activity('a', curr_activ)
  c1 = abstract_activity('c', curr_activ)
  a = time.time()
  for i in range(1000):
    a1.start_activity()
    c1.start_activity()
    a1.stop_activity()
    c1.stop_activity()
    a1.stop_activity()
    a1.start_activity()
    a1.stop_activity()
    print('{} gone'.format(i))
  # print(a1.type, c1.id, a1.status)
  # pprint(db.db)
  db.print()
  b = time.time()
  print(b-a)
  
if __name__ == "__main__":
  main()
