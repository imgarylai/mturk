import ujson
import pandas as pd
import os.path
import glob

with open('classified/0.4.json') as f:
    data = ujson.load(f)

def annotate():
    col = ['ent', 'is_mention', 'result']

    for i, thread in enumerate(data):
        df = pd.DataFrame(columns=col)
        file = 'f1/f1-{}-0.4.csv'.format(i)
        if os.path.exists(file):
            continue
        print("Iteration: {}".format(file))
        for email in thread['emails']:
            print("---------------------------")
            print(email['body'])
            print("---------------------------")
            for ent in email['ents']:
                predict = ent[1] or ent[2] == "PERSON" or ent[2] == "ORG"
                row = [ent]
                if predict:
                    row.append(True)
                else:
                    row.append(False)
                correct = input('Is "{}" a mention?'.format(ent[0]))
                if correct == '1':
                    row.append(True)
                else:
                    row.append(False)

                f1_df = pd.DataFrame([row], columns=col)
                df = df.append(f1_df, ignore_index=True)

        df.to_csv(file, index=False)

def cal_thread():
    print("|Thread|Amount of email|Cumulative amount of email|")
    print("|---|---|---|")
    total_email_count = 0
    for i, thread in enumerate(data):
        email_count = len(list(map(lambda email: email, thread['emails'])))
        total_email_count += email_count
        print("|{}|{}|{}|".format(i+1, email_count, total_email_count))


def cal_f1():
    allFiles = glob.glob("f1/*.csv")
    list_ = []
    for file_ in allFiles:
        df = pd.read_csv(file_, index_col=None, header=0)
        list_.append(df)
    frame = pd.concat(list_)
    TP, FP, FN, TN = 0, 0, 0, 0
    for row in frame.iterrows():
        if row[1].is_mention and row[1].result:
            TP += 1
        elif row[1].is_mention and not row[1].result:
            FP += 1
        elif not row[1].is_mention and row[1].result:
            FN += 1
        elif not row[1].is_mention and not row[1].result:
            TN += 1
    p = TP/(TP + FP)
    r = TP/(TP + FN)
    f1 = 2*TP/(2*TP + FP + FN)
    print("TP: {}, FP: {}, FN: {}, TN: {}".format(TP, FP, FN, TN))
    print("precision: {}".format(p))
    print("recall: {}".format(r))
    print("F1: {}".format(f1))


if __name__ == '__main__':

    # do_annotate = input("Do you want to annotate new data?")
    #
    # if do_annotate == '1':
    #     annotate()
    # else:
    #     cal_f1()
    cal_f1()
    cal_thread()