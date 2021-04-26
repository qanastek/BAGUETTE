stopwords = []

for i in range(1,4):

    filename = str(i) + ".txt"
    print(filename)

    with open(filename) as f:
        content = f.read()
        stopwords += content.split("\n")

f = open("biggest_stopwords_ever.txt", "w")
content = list(set(stopwords))
[f.write(c + "\n") for c in content]
f.close()