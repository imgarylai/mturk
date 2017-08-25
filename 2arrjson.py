import json
import os

version = 2
path = 'classified/v{0}/ents_hq'.format(version)
out_file = 'classified/v{0}/email.threads.strict.only.ents.json'.format(version)


if __name__ == '__main__':
    result = []
    for subdir, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.json'):
                json_file =os.path.join(subdir, file)
                print(json_file)
                with open(json_file) as j:
                    data = json.load(j)

                result.append(data)
    print(result)

    with open(out_file, 'w') as out:
        json.dump(result, out, indent=2)