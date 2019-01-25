import subprocess
import tempfile
import difflib
from django_rq import job
import os
import docker
import requests.exceptions

from catalog.models import Test, Task, Solution, User
from catalog import pubnub_test

# import django
# django.setup()
def delete_files():
    name = 'app.py'
    if os.path.exists(name):
        os.remove(name)
    name = 'app.rb'
    if os.path.exists(name):
        os.remove(name)
    name = 'input.txt'
    if os.path.exists(name):
        os.remove(name)


def create_container(language, name):
    cli = docker.APIClient(base_url='unix://var/run/docker.sock')
    path2 = os.getcwd()+'/input.txt:/app/input.txt'
    # print(language)
    if language == 'Ruby':
        command = 'ruby'
        path = os.getcwd()+'/app.rb:/app/app.rb'
        image='ruby'
    else:
        command = 'python3'
        path = os.getcwd()+'/app.py:/app/app.py'
        image='python:3'
    
    cli.create_container(
        image=image,
        command=[command, name],
        # command=['cat', 'app.py']
        volumes=['/app'],
        host_config=cli.create_host_config(
            binds=[path, path2]
        ),
        name='container_test',
        working_dir='/app',
    )
    try:
        cli.start('container_test')
        status = cli.wait('container_test', timeout=10)
        print('container ', status['StatusCode'])
        if status['StatusCode']:
            raise Exception('Error in the container')
        output = cli.logs('container_test')
        print('try_block_output: ', output)
        cli.remove_container('container_test', force=True)
        return output

    except requests.exceptions.ConnectionError:
        print("runtime")
        cli.remove_container('container_test', force=True)
        return "runtime"

    except Exception as e:
        print('Exeption: ', e)
        cli.remove_container('container_test', force=True)
        return "can't compile"


def exec_file(test_output, language, name):
    logs = create_container(language, name)
    if logs == 'runtime' or logs == "can't compile":
        return [logs]
    logs = logs.decode("utf-8").replace('\n', '\r\n').rstrip()
    
    try:
        assert logs == test_output
    except Exception as e:
        return list(difflib.ndiff(logs, test_output))
    return []


def solution_to_file(solution, test, language):
    if language == 'Ruby':
        name = 'app.rb'
        suffix = '.rb'
        file_prefix = 'file = STDIN.reopen("input.txt")\n'
        file_suffix = '\nfile.close'
    else:
        name = 'app.py'
        suffix = '.py'
        file_prefix = "import sys\nsys.stdin = open('./input.txt')\n"
        file_suffix = ''

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False, mode='w+b') as temp:
        temp.write(bytes(file_prefix + solution + file_suffix,'utf-8'))
        temp.close()
        if os.path.exists(name):
            os.remove(name)
        os.rename(temp.name, name)

        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w+b') as input_file:
            input_file.write(bytes(test.test_input, 'utf-8'))
            if os.path.exists("input.txt"):
                os.remove("input.txt")
            os.rename(input_file.name, 'input.txt')
            input_file.close()

            return exec_file(test.test_output, language, name)


@job
def solution_testing(solution_id):
    print('test_solution')
    solution = Solution.objects.get(pk=solution_id)
    print(solution)
    task = solution.task
    # import pdb; pdb.set_trace()
    tests = [test for test in Test.objects.all() if test.task == task]
    score = 0
    reports = ""
    test_num = len(tests)
    for test in tests:
        res = solution_to_file(solution.solution, test, solution.language)
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
    delete_files()

    print('sent_message')
    print(solution)
    pubnub_test.publish([solution.score, solution_id])
