from datetime import datetime
from time import sleep
from pprint import pprint

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
    self.started = ''
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
    if not self.started:
      self.status = 'run'
      print("started", self.id)
      self.current_active.update(self)
    else:
      print("already start", self.id)
  
  def stop_activity(self):
    if self.started:
      print('stopped', self.id)
      self.status = 'stop'
      self.current_active.update(self)
      self.started = ''
    else:
      print('already stopped', self.id)

class current_activity(object):
  """
  activity with time period in mind
  """
  
  def __init__(self, activity=None, dbo=None):
    print("init current active")
    if activity:
      self.activity = activity
      self.id = activity.id
      self.activity.started = self.get_time()
      self.started = activity.started
      self.stopped = ''
      self.write_start_to_dbo()
    else:
      self.activity = None
      self.id = None
    if dbo:
      self.dbo = dbo
  
  def get_time(self):
    return datetime.utcnow()
  
  def update(self, activity):
    print("update current active", self.id)
    current_date = self.get_time()
    if self.activity:
      self.stopped = current_date
      self.write_stop_to_dbo()
      
    self.activity = activity
    self.id = activity.id
    self.activity.started = current_date
    self.started = current_date
    self.stopped = ''
    self.write_start_to_dbo()
      
  def write_start_to_dbo(self):
    curr_dict = {'id': self.activity.id, 'state': self.activity.status, 'date': self.started}
    self.dbo.append(curr_dict)
    
  def write_stop_to_dbo(self):
    curr_dict = {'id': self.activity.id, 'state': self.activity.status, 'date': self.stopped}
    self.dbo.append(curr_dict)

class DBO(object):
  """
  abstract over database
  """
  
  def __init__(self):
    self.db = []
  
  def append(self, d={}):
    self.db.append(d)


def main():
  db = DBO()
  curr_activ = current_activity(None, dbo=db)
  a1 = abstract_activity('a', curr_activ)
  c1 = abstract_activity('c', curr_activ)
  a1.start_activity()
  sleep(1)
  c1.start_activity()
  sleep(1)
  a1.stop_activity()
  sleep(1)
  a1.start_activity()
  sleep(1)
  a1.stop_activity()
  sleep(1)
  #print(a1.type, c1.id, a1.status)
  pprint(db.db)
  
if __name__ == "__main__":
  main()