# TinyDuck String

- TD is my custom encoding that saves 1 letter as 5 bits and uses 2 swtiches to uppercase and to second collom of table.
- This is simple class that converts from text, or TD to text or TD. 


#### instalation:
´´´
pip install td-string
´´´
#### usage:
´´´
from td_string import TD_string

td = TD_string("This is from string")
td.show()

print(td.bytes)
print(f"Počet bitů - TD    {len(td)*5}")
print(f"Počet bitů - ASCII {len(td)*8}")
print(f"TD je o {100- (len(td)*5/(len(td)*8/100))}% menší")
´´´
