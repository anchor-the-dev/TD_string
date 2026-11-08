import sys
import unicodedata
from pathlib import Path
import jsonlines

# TinyDuck by dduckling

class TD_string:
    def __init__(self, st=None, byt=None, table="cs"):
        if st is None and byt is None:
            print("No vallue asigned")
            sys.exit(1)
        if st is not None:
            self.rawstring = st
            self.string = self._text2ascii(st)
        self.table_load(table)
        self.load_string(st)

    def load_string(self, s):
        """
        load the bits and int tupple from string
        """
        self.intuple = []
        self.btuple = []
        for i in s:
            k = self.letter2numbers(i)
            if k is not None:
                self.intuple.extend(k)
                self.btuple.extend([f"{x:05b}" for x in k])

        self.intuple = tuple(self.intuple)
        self.btuple = tuple(self.btuple)

        n = len(self.btuple)*5 
        d = 8 - (n % 8)
        if d == 0:
            d == 0
        self.bytes = "".join([str(x) for x in self.btuple])
        self.bstr = self.bytes + "0" * d        
        self.bytes = bytes(self.intuple)

    def table_load(self, table):
        path = Path(f"./tables/{table}.jsonl")
        if not path.exists():
            print(f"Table {path} does not exist.")
            sys.exit(1)

        set1 = []
        set2 = []
        with jsonlines.open(path) as f:
            for row in f:
                if "1" in row:
                    set1.extend(row["1"])
                if "2" in row:
                    set2.extend(row["2"])
        self.table = (tuple(set1), tuple(set2))

    def _text2ascii(self, text):
        normalized = unicodedata.normalize('NFD', text)
        ascii_text = "".join(c for c in normalized if unicodedata.category(c) != 'Mn')
        return ascii_text
    
        

    def letter2numbers(self, i):
        r = None
        if i.isupper():
            r = [31] 
        else:
            r = []
        
        try:
            r.append(self.table[0].index(i.lower()))
        except ValueError:
            try:
                r.extend([30 , self.table[1].index(i.lower())])
            except ValueError:
                return None
        return r 

    def __str__(self):
        return self.string

    def __len__(self):
        return len(self.btuple)

    def __getitem__(self, key):
        if not isinstance(key, int):
            raise TypeError("Indices must be integers, not str")

        return self.btuple[key]



i = TD_string("Ahoj jak se mas")
print(i)
print(i.bytes)
