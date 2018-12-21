import time
import django_rq

from catalog.models import Test, Task, SolutionInstance, User
from .additions import test_solution


def rq_exec(solution_id):
    # job = q.enqueue(test_solution, solution, task)
    django_rq.enqueue(test_solution, solution_id)
    # while job.result is None:
    #     time.sleep(1)
