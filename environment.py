from collections import Counter
import random
import secrets
import time

import matplotlib.pyplot as plt
import numpy as np


class Job:
    def __init__(self, duration: int):
        self.duration: int = duration
        self.done: bool = False
        self.id: str = secrets.token_hex()

    def __repr__(self) -> str:
        return f'Job({self.duration})'

    def __isub__(self, num):
        self.duration -= num
        return self


class Cluster:
    def __init__(self, n_machines):
        self.resources = np.zeros(n_machines)
        self.jobs = []

    def add_job(self, job):
        if not isinstance(job, Job):
            raise TypeError(f'job not of type Job but {type(job)}')

        self.jobs.append(job)

    def step(self):
        # time.sleep(0.1)
        zero_array = np.zeros_like(self.resources)
        self.resources = np.maximum(zero_array, self.resources - 1)

    def available_resources(self):
        """Returns random available resource."""
        return np.flatnonzero(self.resources == 0)

    def assign_job(self, resource, job):
        self.resources[resource] = job.duration

    def done(self):
        return len(self.jobs) == 0 and (self.resources == 0).all()

    # More RL-like functions

    def do_action(self, job):
        """Assign given job to random chosen resource and perform time step."""
        available = self.available_resources()
        if len(available) == 0:
            raise ValueError(
                'Not able to perform action, no resources available')

        resource = np.random.choice(available)
        self.assign_job(resource, job)
        self.step()

    def get_actions(self):
        return self.jobs, self.available_resources()

    def state(self):
        return self.jobs, self.resources


def fifo(cluster):
    start = time.time()
    while not cluster.done():
        while (resources := cluster.available_resources()).size > 0 and cluster.jobs:
            resource = np.random.choice(resources)
            new_job = cluster.jobs.pop(0)
            cluster.assign_job(resource, new_job)

        cluster.step()
    print(f'FIFO: Done! time: {time.time() - start} seconds')


def sjf(cluster):
    start = time.time()
    cluster.jobs = sorted(cluster.jobs, key=lambda t: t.duration)
    while not cluster.done():
        while (resources := cluster.available_resources()).size > 0 and cluster.jobs:
            resource = np.random.choice(resources)
            new_job = cluster.jobs.pop(0)
            cluster.assign_job(resource, new_job)

        cluster.step()
    print(f'SJF: Done! time: {time.time() - start} seconds')


def show_data(data):
    c = Counter(data)
    plt.bar(c.keys(), c.values())
    plt.show()


def main():
    cl = Cluster(5)
    cl2 = Cluster(5)
    numbers = []

    for _ in range(5000):
        num = int(30 * random.lognormvariate(0, 0.5))
        numbers.append(num)
        cl.add_job(Job(num))
        cl2.add_job(Job(num))

    fifo(cl)
    sjf(cl2)


if __name__ == '__main__':
    main()
