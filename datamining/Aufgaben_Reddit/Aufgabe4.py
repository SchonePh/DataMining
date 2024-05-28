import pandas as pd
from datetime import datetime

df = pd.read_csv("Aufgaben_Reddit/Aufgabe2.csv")


def delta_post_comment_date(frame, post_date_column, comment_date_column):
    delta = []
    df2 = pd.concat([frame[post_date_column], frame[comment_date_column]], axis=1)
    for idx, row in df2.iterrows():
        post_date = datetime.strptime(row[post_date_column], "%Y-%m-%d %H:%M:%S")
        comment_date = datetime.strptime(row[comment_date_column], "%Y-%m-%d %H:%M:%S")
        delta.append(abs((comment_date - post_date).days))
    df_delta = pd.DataFrame(delta, columns=["date_delta"])
    return df_delta.value_counts()


print(delta_post_comment_date(df, "s_date", "c_date"))
