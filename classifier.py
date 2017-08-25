import ujson
import csv
import os.path

with open("classified/v2/email.threads.strict.only.ents.json") as f:
    data = ujson.load(f)


def cal_reward(l):
    read_instruction = 0.5
    word_count = l * 1 / 30.0
    return round((read_instruction + word_count) / 60.0 * 6.0, 3)


def one_five_round(x):
    return round(x * 10) / 10


if __name__ == '__main__':
    dir_list = []
    prefix = 'classified'
    version = 2
    for thread in data:
        file_name = str(one_five_round(cal_reward(sum(list(map(lambda email: len(email['ents']), thread['emails']))))))
        dir = "{0}/v{1}/{2}".format(prefix, version, file_name)
        file = "{0}/{1}.json".format(dir, file_name)

        if not os.path.isdir(dir):
            dir_list.append(dir)
            os.mkdir(dir)

        if not os.path.exists(file):
            a = []
            with open(file, 'w') as init:
                ujson.dump(a, init)

        with open(file) as inf:
            tmp = ujson.load(inf)

        tmp.append(thread)

        with open(file, 'w') as out:
            ujson.dump(tmp, out, indent=2)

    with open("{0}/v{1}/dir.csv".format(prefix, version), "w") as f:
        writer = csv.writer(f)
        writer.writerow(dir_list)
