import re
text1 = "<@emnesoi#0451> <@flicky🐦#4962> @AnAlternateAccount#0746 @TomtheCatman#9489 @Unbiased Juror#6688 @valtari#0001"
result = re.findall("<.*>", text1)
print(result)