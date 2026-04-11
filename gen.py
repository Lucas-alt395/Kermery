# generator.py

def generate_nasm(ast):
    # We start with the 16-bit Bootloader header for OSDev
    asm = [
        "bits 16",
        "org 0x7C00",
        "",
        "start:",
        "    ; --- Kernel Code ---"
    ]
    
    # We will split data into a separate section at the end
    data_section = ["", "section .data"]
    
    nasm_types = {
        "byte": "db",
        "d-byte": "dw",
        "f-byte": "dd",
        "e-byte": "dq",
        "num": "dd"
    }

    for node in ast:
        if node["type"] == "DECLARE":
            name = node["name"]
            val = node["value"]
            size = nasm_types.get(node["data_type"], "db")
            # In Assembly, variables are usually defined in the data section
            data_section.append(f"    {name} {size} {val}")

    asm.append("    jmp $ ; Infinite loop") # Stop the CPU here
    asm.extend(data_section)
    
    # The Magic Boot Signature (Requirement for BIOS)
    asm.append("")
    asm.append("times 510-($-$$) db 0")
    asm.append("dw 0xAA55")
    
    return "\n".join(asm)
