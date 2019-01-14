import subprocess
import tempfile
import difflib
from django_rq import job
import os
import docker
import requests.exceptions

from catalog.models import Test, Task, SolutionInstance, User
from catalog import pubnub_test


def create_container():
    cli = docker.APIClient(base_url='unix://var/run/docker.sock')
    path = os.getcwd()+'/app.py:/app/app.py'
    path2 = os.getcwd()+'/input.txt:/app/input.txt'
    cli.create_container(
        image='python:3',
        command=['python3', 'app.py'],
        # command=['cat', 'app.py']
        volumes=['/app'],
        host_config=cli.create_host_config(
            binds=[path, path2]
        ),
        name='container_test',
        working_dir='/app'
    )
    try:
        cli.start('container_test')
        cli.wait('container_test', timeout=10)
        output = cli.logs('container_test')
        cli.remove_container('container_test', force=True)

    except requests.exceptions.ConnectionError:
        print("runtime")
        cli.remove_container('container_test', force=True)
        return "runtime"

    except Exception as e:
        cli.remove_container('container_test', force=True)
        return "can't compile"

    # for c in cli.containers.list():
    #     print(c)
    #     c.stop()

    # cli.remove_container('container_test', force=True)
    # cli.stop('container_test')
    print(output)
    return output


def exec_file(test_output):
    logs = create_container()
    if logs == 'runtime' or logs == "can't compile":
        return [logs]
    logs = logs.decode("utf-8").replace('\n', '\r\n').rstrip()
    
    try:
        assert logs == test_output
    except Exception as e:
        return list(difflib.ndiff(logs, test_output))
    return []

    # try:
    #     try:
    #         res.stdin.write(bytes(test_input, 'utf-8'))
    #         output = res.communicate(timeout=15)[0].decode().replace('\n', '\r\n').rstrip()
    #         assert output == test_output
    #         # res.wait(timeout=2)
    #     except subprocess.TimeoutExpired:
    #         print("runtime")
    #         res.kill() 
    #         return ["runtime"]
    #     except Exception as e:
    #         return list(difflib.ndiff(output, test_output))
    #     return []
    # except Exception as e:
    #     return ["can't compile"]


def solution_to_file(solution, test):
    with tempfile.NamedTemporaryFile(suffix='.py', delete=False, mode='w+b') as temp:
        temp.write(bytes("import sys\nsys.stdin = open('./input.txt')\n" + solution,'utf-8'))
        temp.close()
        if os.path.exists("app.py"):
            os.remove("app.py")
        os.rename(temp.name, 'app.py')

        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w+b') as input_file:
            input_file.write(bytes(test.test_input, 'utf-8'))
            if os.path.exists("input.txt"):
                os.remove("input.txt")
            os.rename(input_file.name, 'input.txt')
            input_file.close()
            # print(os.listdir(os.getcwd()))
            return exec_file(test.test_output)


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
    # if os.path.exists("app.py"):
    #     os.remove("app.py")
    # if os.path.exists("input.txt"):
    #     os.remove("input.txt")
    print('sent_message')
    pubnub_test.publish([solution.score, solution_id])
