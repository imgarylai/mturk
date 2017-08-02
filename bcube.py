import ujson
import pandas as pd
import bcubed


class AnswerParseException(LookupError):
    pass


with open('classified/0.1/0.1.json') as f:
    data = ujson.load(f)

df = pd.read_csv('classified/0.1/0.1.mturk.csv')


def get_mentions(email):
    return [ent for ent in email['ents'] if ent[1] or ent[2] == "PERSON" or ent[2] == "ORG"]


def get_receivers(email):
    receivers = []
    for r in ['To', 'Cc', 'Bcc']:
        try:
            res = email[r]
            receivers.extend(res)
        except KeyError:
            continue
    return receivers


def get_answers(thread):
    """

    :param thread:
    :return: answers from mturk
    """
    return df.loc[df['Answer.path'] == thread['path']]


def parse_ans(group, row, j, m, item):

    ans_key = "Answer.q_{}_{}".format(j + 1, m + 1)
    ans = row[ans_key]

    if ans.startswith('s') or ans.startswith('r') or ans.startswith('n'):
        group[item].add(ans)
    elif ans.startswith('m'):
        n = ans.split('_')
        parse_ans(group, row, j, int(n[1])-1, item)
    else:
        raise AnswerParseException("Answer format is invalid")

def compute(title, cdict, ldict):
    """Compute extended BCubed precision and recall, and print the results."""
    precision = bcubed.precision(cdict, ldict)
    recall = bcubed.recall(cdict, ldict)
    fscore = bcubed.fscore(precision, recall)
    print("{}: precision={:.2f}, recall={:.2f}, fscore={:.2f}".format(
        title, precision, recall, fscore))


if __name__ == '__main__':

    precision = 0
    precision_count = 0
    recall = 0
    recall_count = 0
    fscore = 0
    fscore_count = 0
    for i, thread in enumerate(data):
        thread_idx = "Thread: {}".format(i)
        answers = get_answers(thread)
        for j, email in enumerate(thread['emails']):
            title = "Email: {}".format(j)
            mentions = get_mentions(email)
            if len(mentions) == 0:
                continue
            groups = {}
            for idx, row in answers.iterrows():
                i = idx % 2
                groups[i] = {}
                for m, mention in enumerate(mentions):
                    item = "item{}".format(m)
                    groups[i][item] = set()


            for m, mention in enumerate(mentions):
                item = "item{}".format(m)
                for idx, row in answers.iterrows():
                    i = idx % 2
                    parse_ans(groups[i], row, j, m, item)

            cdict = groups[0]
            ldict = groups[1]

            precision += bcubed.precision(cdict, ldict)
            recall += bcubed.recall(cdict, ldict)
            fscore += bcubed.fscore(bcubed.precision(cdict, ldict), bcubed.recall(cdict, ldict))
            precision_count += 1
            recall_count += 1
            fscore_count += 1
            compute(title, cdict, ldict)

    precision = precision/precision_count
    recall = recall/recall_count
    fscore = fscore/fscore_count

    print("precision={:.2f}, recall={:.2f}, fscore={:.2f}".format(
        precision, recall, fscore))
