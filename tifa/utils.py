def isalpha(s):
    for char in s:
        if char.isalpha():
            continue
        return False
    return True
