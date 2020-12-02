from pathlib import Path
import os
import random

from locust import HttpUser, task, between
import logging


def get_project_root() -> str:
    return str(Path(__file__).parent.parent)


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = [line.strip() for line in f.readlines() if line.strip()]
    return content


class User(HttpUser):
    wait_time = between(1, 2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ROOT = get_project_root()
        PATH = os.path.join(ROOT, 'data/conll14st-test-data/noalt/official-2014.combined_incorr.txt')
        self.data = read_file(PATH)

    @task
    def correct(self):
        text = random.choice(self.data)
        with self.client.post('', json={"text": text}) as response:
            if response.status_code != 200:
                logging.info(
                    '{} raised during handling following text:\n{}'.format(str(response.raise_for_status()), text))