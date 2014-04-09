'''Simple (mostly text-related) tools for the cms.'''

def lstripseqonce(s, seq):
 if s.startswith(seq): return s[len(seq):]
 else: return s

def rstripseqonce(s, seq):
 if s.endswith(seq): return s[:-len(seq)]
 else: return s

def replace_multiple(s, replace_pairs):
	for (key, val) in replace_pairs: s = s.replace(key, val)
	return s
