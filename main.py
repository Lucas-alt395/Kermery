from lexer import tokenize, recheck

raw = tokenize("let x be gay gay as string")
recheckd = recheck(raw)

print(recheckd)