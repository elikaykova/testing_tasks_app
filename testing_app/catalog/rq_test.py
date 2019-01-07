import time
import django_rq

from catalog.models import Test, Task, SolutionInstance, User
from .additions import test_solution
from catalog import pubnub_test


def rq_exec(solution_id):
    # solution = SolutionInstance.objects.get(id=solution_id)
    # my_listener = pubnub_test.MySubscribeCallback()
    # pubnub_test.pubnub.add_listener(my_listener)
    # pubnub_test.pubnub.subscribe().channels('submit_channel').execute()

    django_rq.enqueue(test_solution, solution_id)


