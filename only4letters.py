import re
import json

with open("words.txt", "r") as f:
    wl = f.read().splitlines()

result = []

for w in wl:
    if re.match("^....$", w):
        result.append(w)


def one_letter_of_re(w):
    re_string=""
    for n, l in enumerate(w):
        tmpw=list(w)
        tmpw[n]="."
        tmpw="".join(tmpw)
        re_string = re_string + "(^"+tmpw+"$)|"
    re_string = re_string[:-1:]
    return re_string


adjazenzmatix = []
print(f"found {len(result)} four letter words")

for r in result:
    row=[]
    reg = one_letter_of_re(r)
    for u in result:
        if re.match(reg, u) and u!=r:
            row.append(1)
        else:
            row.append(0)
    adjazenzmatix.append(row)

dump = {"words": result, "adjazenzmatrix": adjazenzmatix}

with open('4_letter_words_graph', 'w', encoding="utf-8") as f:
    json.dump(dump, f, ensure_ascii=False, indent=4)