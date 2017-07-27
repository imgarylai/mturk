import pandas as pd
import jinja2
import ujson
import htmlmin
import os.path
import csv

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

    with open('classified/dir.csv', 'r') as f:
        reader = csv.reader(f)
        dir_list = list(reader)

    col = ['question_html']

    for dir in dir_list[0]:
        json = "{}/{}.json".format(dir, os.path.basename(os.path.normpath(dir)))
        file = "{}/{}.csv".format(dir, os.path.basename(os.path.normpath(dir)))
        with open(json) as inf:
            data = ujson.load(inf)

        df = pd.DataFrame(columns=col)

        for thread in data:
            minified = htmlmin.minify(html_question(thread), remove_empty_space=True)
            mturk_df = pd.DataFrame([[minified]], columns=col)
            df = df.append(mturk_df, ignore_index=True)

        df.to_csv(file, index=False)
