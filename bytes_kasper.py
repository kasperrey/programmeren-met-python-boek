bytes_teken = '\³'
x = 'x'
c = ''
_bytes = ''
hallo = str(input("welke string wil je weten"))
hallo_bytes = bytes(hallo, 'utf-8')
class strings_omzetten_naar_bytes:
    def forlussen(string, c, _bytes):
        for byte in hallo_bytes:
            c = "".join([c, bytes_teken, x, str(byte)])
        for s in c:
            if s == '>':
                continue
            _bytes = "".join([_bytes, s])
            return _bytes

class bytes_omzetten_naar_strings(strings_omzetten_naar_bytes):
    def makkie():
        string = _bytes.decode('utf-8')
        return string

jef = strings_omzetten_naar_bytes
jef.forlussen(hallo_bytes, c, _bytes)
jopiër = bytes_omzetten_naar_strings
jopiër.makkie()
