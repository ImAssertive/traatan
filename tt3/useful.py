def getid(mention):
    id = int("".join(each for each in mention if each.isdigit()))
    return id

def formatText(ctx, text):
    return text.replace("%user%", ctx.mention)

def getMenuEmoji(noOfOptions):
    emojis = [["one", "1\u20e3"],["two", "2\u20e3"],["three", "3\u20e3"],["four", "4\u20e3"], ["five", "5\u20e3"],["six", "6\u20e3"], ["seven", "7\u20e3"],["eight", "8\u20e3"],["nine", "9\u20e3"],["ten", "\U0001f51f"]]
    toReturn = []
    for i in range (0,noOfOptions):
        toReturn.append(emojis[i])
    toReturn.append(["x", "❌"])
    return toReturn