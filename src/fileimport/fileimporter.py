#!/usr/bin/python
#
# Copyright (C) 2010 Google Inc.

""" Imports files.

Imports CSV files into Fusion Tables.
"""

__author__ = 'kbrisbin@google.com (Kathryn Brisbin)'


from sql.sqlbuilder import SQL

class Importer:
  def importFile(self, filename):
    pass
  
  def importMoreRows(self, filename):
    pass
  
  

class CSVImporter(Importer):
  def __init__(self, ftclient):
    self.ftclient = ftclient
  
  def importFile(self, filename, table_name=None, data_types=None):
    """ Creates new table and imports data from CSV file """
    filehandle = open(filename, "r")
    cols = filehandle.readline().strip().split(",")
    if data_types: columns_and_types = [(c, d) for c,d in zip(cols, data_types)]
    else: columns_and_types = [(c, "STRING") for c in cols]

    results = self.ftclient.query(SQL().createTable(table_name or filename, columns_and_types))
    table_id = int(results.split()[1])
    
    self._importRows(filehandle, table_id, cols)
    
    return table_id
  
  
  def importMoreRows(self, filename, table_id):
    """ Imports more rows in a CSV file to an existing table. First row is a header """
    filehandle = open(filename)
    cols = filehandle.readline().strip().split(",")
    
    return self._importRows(filehandle, table_id, cols)
  
  
  def _importRows(self, filehandle, table_id, cols):
    """ Helper function to upload rows of data in a CSV file to a table """
    max_per_batch = 500
    current_row = 0
    line = filehandle.readline()
    queries = []
    rows = []
    while line != "":
      values = [value.strip().replace("'", "") for value in line.split(",")]
      query = SQL().insert(table_id, cols, values)
      queries.append(query)
      current_row += 1
      if current_row == max_per_batch: 
        full_query = ';'.join(queries)
        rows += self.ftclient.query(full_query).split("\n")[1:-1]
        current_row = 0
        queries = []
      line = filehandle.readline()
   
    if len(queries) > 0: 
      full_query = ';'.join(queries)
      rows += self.ftclient.query(full_query).split("\n")[1:-1]
      
    return rows
          
if __name__ == "__main__":
  pass
  
  
  