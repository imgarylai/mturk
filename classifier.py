import ujson
import os.path

with open("email.threads.strict.only.ents.json") as f:
    data = ujson.load(f)


def cal_reward(l):
    read_instruction = 3.0
    word_count = l * 1 / 30.0
    return round((read_instruction + word_count) / 60.0 * 6.0, 2)


def one_five_round(x):
    return round(x * 5) / 5


if __name__ == '__main__':
    for thread in data:
        file = "{}.json".format(
            one_five_round(cal_reward(sum(list(map(lambda email: len(email['ents']), thread['emails']))))))

        if not os.path.exists(file):
            a = []
            with open(file, 'w') as init:
                ujson.dump(a, init)

        with open(file) as inf:
            tmp = ujson.load(inf)

        tmp.append(thread)

        with open(file, 'w') as outf:
            ujson.dump(tmp, outf)
