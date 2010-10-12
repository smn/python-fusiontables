#!/usr/bin/python
#
# Copyright (C) 2010 Google Inc.

""" Builds SQL strings.

Builds SQL strings to pass to FTClient query method.
"""

__author__ = 'kbrisbin@google.com (Kathryn Brisbin)'


import re

class SQL:
  """ Helper class for building SQL queries """
      
  def showTables(self):
    """ Build a SHOW TABLES sql statement.
    
    Returns:
      the sql statement
    """
    return 'SHOW TABLES'
  
  def describeTable(self, table_id):
    """ Build a DESCRIBE <tableid> sql statement.
    
    Args:
      table_id: the ID of the table to describe
      
    Returns:
      the sql statement 
    """
    return 'DESCRIBE %d' % (table_id)
  
  def createTable(self, table_name, cols_and_datatypes): 
    """ Build a CREATE TABLE sql statement.
    
    Args: 
      table_name: a name to give to the new table
      cols_and_datatypes: a list of column name, data type pairs.
        for example, [("Name", "STRING"), ("Age", "NUMBER")]
      
    Returns:
      the sql statement
    """
    cols_and_datatypes = ",".join(["'%s': %s" % (col[0], col[1]) for col in cols_and_datatypes])
    return "CREATE TABLE '%s' (%s)" % (table_name, cols_and_datatypes)
  
  
  def select(self, table_id, cols=None, condition=None): 
    """ Build a SELECT sql statement.
    
    Args:
      table_id: the id of the table
      cols: a list of columns to return. If None, return all
      condition: a statement to add to the WHERE clause. For example, 
        "age > 30" or "Name = 'Steve'". Use single quotes as per the API.
        
    Returns:
      the sql statement
    """
    stringCols = "*"
    if cols: stringCols = ','.join(["'%s'" % (col) for col in cols])
    if condition: select = 'SELECT %s FROM %d WHERE %s' % (stringCols, table_id, condition)
    else: select = 'SELECT %s FROM %d' % (stringCols, table_id)
    return select
      
  
  def update(self, table_id, cols, values, row_id):
    """ Build an UPDATE sql statement.
    
    Args: 
      table_id: the id of the table
      cols: the columns to update
      values: the new values
      row_id: the id of the row to update
      
    Returns:
      the sql statement
    """
    if len(cols) != len(values): return None
    updateStatement = ""
    count = 1
    for i in range(len(cols)):
        updateStatement += "'" + cols[i] + "' = "
        if type(values[i]).__name__=='int' or type(values[i]).__name__=='float':
            updateStatement += str(values[i])
        else: 
            updateStatement += "'%s'" % (str(values[i]))
            
        if count < len(cols): updateStatement += ","
        count += 1
    
    return "UPDATE %d SET %s WHERE ROWID = '%d'" % (table_id, updateStatement, row_id)
      
  def delete(self, table_id, row_id):
    """ Build DELETE sql statement.
    
    Args: 
      table_id: the id of the table
      row_id: the id of the row to delete
      
    Returns:
      the sql statement
    """    
    return "DELETE FROM %d WHERE ROWID = '%d'" % (table_id, row_id)
  
  
  def insert(self, table_id, cols, values): 
    """ Build an INSERT sql statement.
    
    Args: 
      table_id: the id of the table
      cols: the cols to insert data into
      values: the values
      
    Returns:
      the sql statement
    """ 
    stringValues = ""
    count = 1
    for value in values:
        if type(value).__name__=='int' or type(value).__name__=='float': stringValues += str(value)
        else: stringValues += "'%s'" % (re.sub(r"(?<!\\)'", "\\'", str(value))) 
        if count < len(values): stringValues += ","
        count += 1
    
    return 'INSERT INTO %d (%s) VALUES (%s)' % (table_id, ','.join(["'%s'" % col for col in cols]), stringValues)
      
  def dropTable(self, table_id): 
    """ Build DROP TABLE sql statement.
    
    Args: 
      table_id: the id of the table
      
    Returns:
      the sql statement
    """ 
    return "DROP TABLE %d" % (table_id)
  
    
if __name__ == '__main__':
    pass
    
    
    
