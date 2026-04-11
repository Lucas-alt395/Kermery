import re
import sys

# The tokenize function will give you a list of tokens!
def tokenize(code):
    # Let's remove the comments!
    code = re.sub(r'//.*', '', code) 

    # Chop it into pieces...
    pattern = r'[a-zA-Z0-9-]+|\{|\}|\(|\)|\:|\".*?\"'
    words = re.findall(pattern, code)
    
    tokens = []
    
    # and give them some IDs!
    for word in words:
        if word == "let": tokens.append(("KW_LET", word))
        elif word == "be": tokens.append(("KW_BE", word))
        elif word == "as": tokens.append(("KW_AS", word))
        elif word == "set": tokens.append(("KW_SET", word))
        elif word == "get": tokens.append(("KW_GET", word))
        elif word == "function": tokens.append(("KW_FUNC", word))
        elif word == "pass": tokens.append(("KW_PASS", word))
        elif word == "asm": tokens.append(("KW_ASM", word))
        elif word == "(": tokens.append(("L_PAREN", word))
        elif word == ")": tokens.append(("R_PAREN", word))
        elif word == "{": tokens.append(("L_BRACE", word))
        elif word == "}": tokens.append(("R_BRACE", word))
        elif word == ":": tokens.append(("COLON", word))
        elif word.isdigit(): tokens.append(("VALUE_NUM", int(word)))
        elif word.startswith('"'): tokens.append(("VALUE_STR", word.strip('"')))
        else: tokens.append(("POSSIBLE_IDENTIFIER", word))
            
    return tokens

# The recheck function is specifically for types, values and identifiers, to give them some own tags.
def recheck(tokens):
    RESERVED_TYPES = {"byte", "d-byte", "f-byte", "e-byte", "alpha", "string", "char", "num"}
    final_tokens = []

    # Set some var.s to know when we are expecting an id, a type or an value, so they all have their own tags
    global identifierSoon
    identifierSoon = False
    global specSoon
    specSoon = False
    global valueSoon
    valueSoon = False

    for tag, value in tokens:
        if tag == "KW_LET":
            identifierSoon = True
        if tag == "KW_BE":
            valueSoon = True          
        if tag == "KW_AS":
            specSoon = True
        
        if tag == "POSSIBLE_IDENTIFIER":
            if identifierSoon:
                final_tokens.append(("IDENTIFIER", value))
                identifierSoon = False
            elif specSoon:
                final_tokens.append(("TYPE_SPEC", value))
                specSoon = False
            elif valueSoon:
                if value in RESERVED_TYPES:
                    sys.exit(f"Lexer (recheck) Error: An value cannot be named after a reserved type. ({value})")
                else:
                    final_tokens.append(("VALUE_IDENTIFIER", value))
                valueSoon = False
            else:
                sys.exit(f"Lexer (recheck) Error: An possible identifier does not have the keyword 'let', 'be' or 'as' before it. ({value})")
        else:
            final_tokens.append((tag, value))
    return final_tokens
