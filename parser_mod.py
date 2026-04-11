# parser_mod.py

class Parser:
    def __init__(self, tokens, sbk_library):
        self.tokens = tokens
        self.pos = 0
        self.sbk_library = sbk_library

    def peek(self, offset=0):
        if self.pos + offset >= len(self.tokens):
            return (None, None)
        return self.tokens[self.pos + offset]

    def consume(self, expected_tag=None):
        tag, value = self.peek()
        if expected_tag and tag != expected_tag:
            raise Exception(f"Syntax Error: Expected {expected_tag} but got {tag} at token {self.pos}")
        self.pos += 1
        return tag, value

    def parse(self):
        ast = []
        while self.pos < len(self.tokens):
            tag, value = self.peek()

            if tag == "KW_LET":
                ast.append(self.parse_let())
        
            # NEW: Check if this is a function call (Identifier + '(' )
            elif tag == "IDENTIFIER" and self.peek(1)[0] == "L_PAREN":
                # Call a new method we'll create
                ast.append(self.parse_module_call()) 
            
            elif tag == "KW_FUNC":
                ast.append(self.parse_function())
            
            else:
                print(f"Warning: Unrecognized token: {self.peek()}. This might cause issues later.")
                self.pos += 1 
        return ast


    def parse_let(self):
        self.consume("KW_LET")
        _, name = self.consume("IDENTIFIER")
        self.consume("KW_BE")
        val_tag, val_value = self.consume()
        
        var_type = "num"
        if self.peek()[0] == "KW_AS":
            self.consume("KW_AS")
            _, var_type = self.consume("TYPE_SPEC")
            
        return {"type": "DECLARE", "name": name, "value": val_value, "data_type": var_type}

    def parse_module_call(self):
        func_name = self.consume("IDENTIFIER")[1]
        self.consume("L_PAREN")
    
        arg = ""
        if self.peek()[0] != "R_PAREN":
            _, arg = self.consume() # Get the 'A'
    
        self.consume("R_PAREN")

        # Look up in our JSON (self.sbk_library)
        # We strip the () from the JSON keys to match
        asm_template = ""
        for key, asm in self.sbk_library["functions"].items():
            if key.startswith(func_name):
                asm_template = asm
                break

        # Swap [val] for the actual argument
        final_asm = asm_template.replace("[val]", str(arg))
        return {"type": "INLINE_ASM", "code": final_asm}

