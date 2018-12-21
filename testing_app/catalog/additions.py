from catalog.models import Test, Task, SolutionInstance, User
import subprocess
import tempfile
import difflib
from django_rq import job


def exec_file(file, test = []):
    test_input = test.test_input
    test_output = test.test_output
    res = subprocess.Popen(['python', file.name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        if res.returncode:
            return ["can't compile"]
        else:
            res.stdin.write(bytes(test_input, 'utf-8'))
            # res.stdin.write(test_input.encode('utf-8'))
            output = res.communicate()[0].decode().replace('\n', '\r\n').rstrip()
            try:
                assert output == test_output
            except Exception as e:
                return list(difflib.ndiff(output, test_output))
            return []
    except Exception as e:
        return ["can't compile"]


def solution_to_file(solution, test):
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w+b') as temp:
        temp.write(bytes(solution, 'utf-8'))
        # temp.write(solution.encode('utf-8'))
        temp.close()
        return exec_file(temp, test)


@job
def test_solution(solution_id):
    solution = SolutionInstance.objects.get(id=solution_id)
    task = solution.task
    # import pdb; pdb.set_trace()
    tests = [test for test in Test.objects.all() if test.task == task]
    score = 0
    reports = ""
    test_num = len(tests)
    for test in tests:
        res = solution_to_file(solution.solution, test)
        if res:
            reports = reports + 'For test {} diffs:'.format(test.test_num) + str(res) + '\n'
        else:
            # reports = reports + 'For test {} diffs:'.format(test.test_num) + str(res)
            score = score + 1

    solution.score = format(score/test_num, '.2f')
    solution.reports = reports
    solution.done = True
    solution.save()
    