import time
import django_rq
import django
django.setup()

from .additions import solution_testing

def rq_exec(solution_id):
    print('queue: enter')
    django_rq.enqueue(solution_testing, solution_id)
