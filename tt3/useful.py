def getid(mention):
    id = int("".join(each for each in mention if each.isdigit()))
    return id

def formatText(ctx, text):
    return text.replace("%user%", ctx.mention)