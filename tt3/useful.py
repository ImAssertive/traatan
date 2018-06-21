def getid(mention):
    id = int("".join(each for each in mention if each.isdigit()))
    return id

