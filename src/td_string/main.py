import sys
import unicodedata
from pathlib import Path
import jsonlines

# TinyDuck by dduckling

class TD_string:
    def __init__(self, st=None, byt=None, table_path=None, table="cs"):
        """
        If table_path is not None it will have higher priority then table.
        """
        if st is None and byt is None:
            print("No vallue asigned")
            sys.exit(1)
        if table_path is None: 
            self.table_load(Path(__file__).parent / "tables" / f"{table}.jsonl")
        else:
            self.table_load(Path(table))

        if st is not None:
            self.rawstring = st
            self.string = self._text2ascii(st)
            self.load_string(st)
        
        if byt is not None:
            self.load_bytes(byt)
        

    def load_bytes(self, b):
        bit_str = "".join(f"{x:08b}" for x in b) 
        st = ""
        upper = False
        second = False
         
        p = len(bit_str) // 5
        for i in range(p):
            current = bit_str[i * 5 : (i + 1) * 5]
            if not current or len(current) < 5:
                break
            cislo = int(current, 2)

            if cislo == 31:
                upper = True
                continue
            if cislo == 30:
                second = True
                continue


            if second:
                second = False
                s = self.table[1][cislo]
            else:
                s = self.table[0][cislo]
            
            if upper:
                upper = False 
                s = s.upper()
            st = st + s
                        
            
            
        self.load_string(st)
        


    def load_string(self, s):
        """
        load the bits and int tupple from string
        """
        self.string = s
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
            d = 0

        self.td = "".join([str(x) for x in self.btuple])
        self.bstr = self.td + "1" * d        

        byte_array = bytearray()
        for i in range(0, len(self.bstr), 8):
            byte_chunk = self.bstr[i:i+8]
            byte_array.append(int(byte_chunk, 2))
        self.bytes = bytes(byte_array)


    def table_load(self, path):
        path = Path(path)
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
if __name__=="__main__":
    string = "ABCDEFGHIJKLMOPQRSTUVWXYZabcdefghijklmopqrstuvwxyz123456890"
    i = TD_string(string)
    print(i)
    print(f"Počet bitů - TD    {len(i)*5}")
    print(f"Počet bitů - ASCII {len(i)*8}")
    print(f"TD je o {100- (len(i)*5/(len(i)*8/100))}% menší")

