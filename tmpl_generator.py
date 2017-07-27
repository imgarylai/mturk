import pandas as pd
import jinja2
import ujson
import htmlmin
import os.path


def render(tpl_path, thread):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(thread=thread)


def html_question(thread):
    for email in thread['emails']:
        receivers = []
        for r in ['To', 'Cc', 'Bcc']:
            try:
                res = email[r]
                receivers.extend(res)
            except KeyError:
                continue
        email['receivers'] = receivers
    return render('question.html', thread)


if __name__ == '__main__':
    with open('classified/0.4.json') as inf:
        data = ujson.load(inf)

    # max_col_nums = max(
    #     list(map(
    #         lambda thread: sum(
    #             list(map(
    #                 lambda email: sum(list(map(
    #                     lambda ent: ent[1] or ent[2] == 'PERSON' or ent[2] == 'ORG', email['ents']
    #                 ))), thread['emails'])
    #             )
    #         ), data)
    #     )
    # )

    col = ['question_html']

    # for i in range(max_col_nums):
    #     col.append("question_{}".format(i + 1))

    print(col)
    df = pd.DataFrame(columns=col)
    # print(df)

    for thread in data:
        minified = htmlmin.minify(html_question(thread), remove_empty_space=True)
    #     ents = []
    #     for email in thread['emails']:
    #         for ent in email['ents']:
    #             if ent[1] or ent[2] == 'PERSON' or ent[2] == 'ORG':
    #                 ents.append(ent[0])
    #
    #     # print(ents)
    #     ents += ["DO NOT ANSWER"] * (max_col_nums - len(ents))
    #     # print(ents)
    #     row = [minified] + ents
    #     # print(row)
    #     mturk_df = pd.DataFrame([row],
    #                             columns=col)
    #     df = df.append(mturk_df, ignore_index=True)

        mturk_df = pd.DataFrame([[minified]],
                                columns=col)
        df = df.append(mturk_df, ignore_index=True)

    df.to_csv('0.4.csv', index=False)
