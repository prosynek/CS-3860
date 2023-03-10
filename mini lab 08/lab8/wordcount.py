import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    #key = record[0] ## our test.json and dec.json files don't use keys
    #value = record[1]
    value = record[0]
    words = value.split()
    for w in words:
      if len(w) == 1:
        mr.emit_intermediate('tiny', 1)
      elif len(w) > 1 and len(w) <= 4:
        mr.emit_intermediate('small', 1)
      elif len(w) >= 5 and len(w) <= 9:
        mr.emit_intermediate('medium', 1)
      elif len(w) >= 10:
        mr.emit_intermediate('big', 1)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    total = 0
    for v in list_of_values:
      total += v
    mr.emit((key, total))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open('dec.json', 'r')
    mr.execute(inputdata, mapper, reducer)
