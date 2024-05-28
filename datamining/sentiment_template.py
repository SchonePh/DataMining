def get_sentiment(sentimentanalyzer, comment):
    """
    Function to calculate the sentiment of a comment.
    :param sentimentanalyzer: the analyzer
    :param comment: the comment for which the sentiment should be calculated
    :return: 1 : compound score >= 0.05
        0 : (compound score > -0.05) and (compound score < 0.05)
        -1 : compound score <= -0.05
    """


def transform(frame, column):
    """
    Function to transform the value of a given column to low, medium and high based on the quantiles:
    <=25 quantile ->-1
    25<x<=75 quantile -> 0
    >75 quantile -> 1
    :param frame: A dataframe
    :param column: Column to transform
    :return: original frame with the transformed
    """


def calc_comments_length(frame, col_name):
    """
    Calculates the length of a text in the given column
    :param frame: A dataframe
    :param col_name: The name of column with the text
    :return: the original frame plus a column "n_letters"
    """
