import pandas as pd

df = pd.read_csv("Aufgaben_Reddit/Aufgabe2.csv")

def calc_comments_length(frame, col_name):
    comments = frame[col_name]
    comment_lengths = []
    for comment in comments:
        comment_lengths.append(len(comment))
    pf2 = pd.DataFrame(comment_lengths, columns=["n_letters"])
    
    return pd.concat([frame, pf2], axis=1)

print(calc_comments_length(df, "c_text"))