import subprocess
import tempfile
import difflib
from django_rq import job

from catalog.models import Test, Task, SolutionInstance, User
from catalog import pubnub_test


def exec_file(file, test = []):
    test_input = test.test_input
    test_output = test.test_output
    res = subprocess.Popen(['python', file.name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        try:
            res.stdin.write(bytes(test_input, 'utf-8'))
            output = res.communicate(timeout=15)[0].decode().replace('\n', '\r\n').rstrip()
            assert output == test_output
            # res.wait(timeout=2)
        except subprocess.TimeoutExpired:
            print("runtime")
            res.kill() 
            return ["runtime"]
        except Exception as e:
            return list(difflib.ndiff(output, test_output))
        return []
    except Exception as e:
        return ["can't compile"]


def solution_to_file(solution, test):
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w+b') as temp:
        temp.write(bytes(solution, 'utf-8'))
        temp.close()
        return exec_file(temp, test)


@job
def test_solution(solution_id):
    print('test_solution')
    solution = SolutionInstance.objects.get(pk=solution_id)
    task = solution.task
    # import pdb; pdb.set_trace()
    tests = [test for test in Test.objects.all() if test.task == task]
    score = 0
    reports = ""
    test_num = len(tests)
    for test in tests:
        res = solution_to_file(solution.solution, test)
        print(res)
        if res:
            reports = reports + 'For test {} diffs:'.format(test.test_num) + str(res) + '\n'
        else:
            score = score + 1

    solution.score = format(score/test_num, '.2f')
    solution.reports = reports
    solution.done = True
    solution.user.update_score(float(solution.score), solution.task)
    solution.user.save()
    solution.save()
    
    print('sent_message')
    pubnub_test.publish([solution.score, solution_id])
