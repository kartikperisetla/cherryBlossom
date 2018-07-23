OLD_VOCAB_FILE = "/Users/kartik/im2txt_2/word_counts.txt"
NEW_VOCAB_FILE = "/Users/kartik/im2txt_2/word_counts_new.txt"

with open(OLD_VOCAB_FILE, "r", encoding="utf-8") as f:
    lines = list(f.readlines())

def clean_line(line):
    # eval_line = eval(line)
    tokens = line.split()
    key = eval(tokens[0]).decode("utf-8")
    val = tokens[1]
    return "%s %s" % (key, val)

newlines = [clean_line(line) for line in lines]

with open(NEW_VOCAB_FILE, "w", encoding="utf-8") as f:
    for line in newlines:
        f.write(line + "\n")

print("vocab cleaned successfully.")