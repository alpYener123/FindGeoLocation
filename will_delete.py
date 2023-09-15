with open(".gitignore", "rb") as file:
    content = file.read()

    if b'\r\n' in content:
        print ("Windows (CRLF)")
    elif b'\n' in content:
        print ("Unix (LF)")
    else:
        print ("Unknown")


