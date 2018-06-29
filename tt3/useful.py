def getid(mention):
    id = int("".join(each for each in mention if each.isdigit()))
    return id

def formatText(ctx, text):
    return text.replace("%user%", ctx.mention)

def getMenuEmoji():
    emojis = [["no_entry", "⛔"]]
    return emojis