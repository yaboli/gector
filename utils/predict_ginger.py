import requests
import argparse
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time


def read_file(path):
    data = []
    with open(path, 'r', encoding='utf-8') as fi:
        for row in fi:
            if row.strip():
                data.append(row.strip())
    return data


def write_to_file(iterable, path):
    if os.path.exists(path):
        os.remove(path)
    with open(path, 'w') as fo:
        for x in iterable:
            if x.strip():
                fo.write(x + '\n')


def fetch(session, input_dict):
    with session.post(url, json={
        "language": "eng",
        "text": input_dict['text'],
        "autoReplace": True,
        "interfaceLanguage": "en",
        "locale": "Indifferent",
        "origin": "interactive",
        "generateSynonyms": False,
        "getCorrectionDetails": True
    }) as response:
        correction = response.json()['text']
        return {'id': input_dict['id'], 'correction': correction}


async def get_data_asynchronous(input_dicts):
    output_dicts = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        with requests.Session() as session:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    fetch,
                    *(session, input_dict)
                )
                for input_dict in input_dicts
            ]
            for response in await asyncio.gather(*tasks):
                output_dicts.append(response)
    return output_dicts


def main():
    input_data = read_file(args.input)
    input_dicts = []
    for i in range(len(input_data)):
        input_dict = {'id': i, 'text': input_data[i]}
        input_dicts.append(input_dict)

    start_time = time.time()

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous(input_dicts))
    output_dicts = loop.run_until_complete(future)

    duration = time.time() - start_time
    print(f"Finished {len(input_data)} in {duration} seconds")

    # output_dicts.sort(key=lambda x: x.id)
    corrections = [x['correction'] for x in output_dicts]

    write_to_file(corrections, args.output)


# def main():
#     input_data = read_file(args.input)
#     corrections = []
#     for i in tqdm(range(len(input_data))):
#         text = input_data[i]
#         data = {
#             "language": "eng",
#             "text": text,
#             "autoReplace": True,
#             "interfaceLanguage": "en",
#             "locale": "Indifferent",
#             "origin": "interactive",
#             "generateSynonyms": False,
#             "getCorrectionDetails": True
#         }
#         r = requests.post(url, json=data)
#         try:
#             r_json = r.json()
#             corrections.append(r_json['text'])
#         except Exception as e:
#             print(str(e))
#
#     write_to_file(corrections, args.output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='/home/yli/gector/data/synthetic/newsgcca-en-fr.en/dev/incorr_sentences.txt')
    parser.add_argument('--output', default='/home/yli/gector/data/ginger/results/newsgcca-en-fr.en.dev.ginger.txt')
    args = parser.parse_args()
    url = 'https://orthographe.reverso.net/api/v1/Spelling'
    main()
