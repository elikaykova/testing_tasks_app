import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db
from django.test import RequestFactory
from django.test import TestCase
from django.utils import timezone
import tempfile
import os
import docker
import time

from catalog import additions
from catalog import models
from catalog import pubnub_test

@pytest.mark.django_db
class PubnubTest(TestCase):
    def test_publish(self):
        pass

@pytest.mark.django_db
class AdditionsTest(TestCase):
    def test_delete_files_rb(self):
        with tempfile.NamedTemporaryFile(delete=False, mode='w+b') as temp:
            temp.close()
            os.rename(temp.name, 'app.rb')
        additions.delete_files()
        assert os.path.exists('app.rb') == False

    def test_delete_files_py(self):
        with tempfile.NamedTemporaryFile(delete=False, mode='w+b') as temp:
            temp.close()
            os.rename(temp.name, 'app.py')
        additions.delete_files()
        assert os.path.exists('app.py') == False

    def test_delete_files_txt(self):
        with tempfile.NamedTemporaryFile(delete=False, mode='w+b') as temp:
            temp.close()
            os.rename(temp.name, 'input.txt')
        additions.delete_files()
        assert os.path.exists('input.txt') == False

    def test_create_container_rb(self):
        name = 'app.rb'
        suffix = '.rb'
        file_prefix = 'file = STDIN.reopen("input.txt")\n'
        file_suffix = '\nfile.close'
        solution = 'a = gets\nprint(a.chomp)\n'

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False, mode='w+b') as temp:
            temp.write(bytes(file_prefix + solution + file_suffix,'utf-8'))
            temp.close()
            if os.path.exists(name):
                os.remove(name)
            os.rename(temp.name, name)

            with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w+b') as input_file:
                input_file.write(bytes('test_input', 'utf-8'))
                if os.path.exists("input.txt"):
                    os.remove("input.txt")
                os.rename(input_file.name, 'input.txt')
                input_file.close()

                res = additions.create_container('Ruby', 'app.rb')
                res = res.decode("utf-8").replace('\n', '\r\n').rstrip()
                assert res == 'test_input'


    def test_create_container_py(self):
        name = 'app.py'
        suffix = '.py'
        file_prefix = "import sys\nsys.stdin = open('./input.txt')\n"
        file_suffix = ''
        solution = 'a = input()\nprint(a)\n'

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False, mode='w+b') as temp:
            temp.write(bytes(file_prefix + solution + file_suffix,'utf-8'))
            temp.close()
            if os.path.exists(name):
                os.remove(name)
            os.rename(temp.name, name)

            with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w+b') as input_file:
                input_file.write(bytes('test_input', 'utf-8'))
                if os.path.exists("input.txt"):
                    os.remove("input.txt")
                os.rename(input_file.name, 'input.txt')
                input_file.close()

                res = additions.create_container('Python', 'app.py')
                res = res.decode("utf-8").replace('\n', '\r\n').rstrip()
                assert res == 'test_input'

    def test_create_container_runtime(self):
        name = 'app.py'
        suffix = '.py'
        file_prefix = "import sys\nsys.stdin = open('./input.txt')\n"
        file_suffix = ''
        solution = 'import time\ntime.sleep(15)\n'

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False, mode='w+b') as temp:
            temp.write(bytes(file_prefix + solution + file_suffix,'utf-8'))
            temp.close()
            if os.path.exists(name):
                os.remove(name)
            os.rename(temp.name, name)

            with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w+b') as input_file:
                input_file.write(bytes('test_input', 'utf-8'))
                if os.path.exists("input.txt"):
                    os.remove("input.txt")
                os.rename(input_file.name, 'input.txt')
                input_file.close()

                res = additions.create_container('Python', 'app.py')
                assert res == 'runtime'

    def test_create_container_can_not_compile(self):
        name = 'app.py'
        suffix = '.py'
        file_prefix = "import sys\nsys.stdin = open('./input.txt')\n"
        file_suffix = ''
        solution = 'time.sleep(1)\n'

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False, mode='w+b') as temp:
            temp.write(bytes(file_prefix + solution + file_suffix,'utf-8'))
            temp.close()
            if os.path.exists(name):
                os.remove(name)
            os.rename(temp.name, name)

            with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w+b') as input_file:
                input_file.write(bytes('test_input', 'utf-8'))
                if os.path.exists("input.txt"):
                    os.remove("input.txt")
                os.rename(input_file.name, 'input.txt')
                input_file.close()

                res = additions.create_container('Python', 'app.py')
                assert res == "can't compile"

    def test_exec_file_can_not_compile(self):
        test_output = 'test_output'
        language = 'Python'
        name = 'app.py'
        suffix = '.py'
        file_prefix = "import sys\nsys.stdin = open('./input.txt')\n"
        file_suffix = ''
        solution = 'time.sleep(1)\n'

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False, mode='w+b') as temp:
            temp.write(bytes(file_prefix + solution + file_suffix,'utf-8'))
            temp.close()
            if os.path.exists(name):
                os.remove(name)
            os.rename(temp.name, name)

            with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w+b') as input_file:
                input_file.write(bytes('test_input', 'utf-8'))
                if os.path.exists("input.txt"):
                    os.remove("input.txt")
                os.rename(input_file.name, 'input.txt')
                input_file.close()

                res = additions.exec_file(test_output, language, name)
                assert res == ["can't compile"]

    def test_exec_file_right_answer(self):
        test_output = 'test_output'
        language = 'Python'
        name = 'app.py'
        suffix = '.py'
        file_prefix = "import sys\nsys.stdin = open('./input.txt')\n"
        file_suffix = ''
        solution = 'a = input()\nprint(a)\n'

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False, mode='w+b') as temp:
            temp.write(bytes(file_prefix + solution + file_suffix,'utf-8'))
            temp.close()
            if os.path.exists(name):
                os.remove(name)
            os.rename(temp.name, name)

            with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w+b') as input_file:
                input_file.write(bytes('test_output', 'utf-8'))
                if os.path.exists("input.txt"):
                    os.remove("input.txt")
                os.rename(input_file.name, 'input.txt')
                input_file.close()

                res = additions.exec_file(test_output, language, name)
                assert res == []

    def test_exec_file_wrong_answer(self):
        test_output = 'out'
        language = 'Python'
        name = 'app.py'
        suffix = '.py'
        file_prefix = "import sys\nsys.stdin = open('./input.txt')\n"
        file_suffix = ''
        solution = 'a = input()\nprint(a)\n'

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False, mode='w+b') as temp:
            temp.write(bytes(file_prefix + solution + file_suffix,'utf-8'))
            temp.close()
            if os.path.exists(name):
                os.remove(name)
            os.rename(temp.name, name)

            with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w+b') as input_file:
                input_file.write(bytes('in', 'utf-8'))
                if os.path.exists("input.txt"):
                    os.remove("input.txt")
                os.rename(input_file.name, 'input.txt')
                input_file.close()

                res = additions.exec_file(test_output, language, name)
                assert res == ['- i', '- n', '+ o', '+ u', '+ t']

    def test_solution_to_file_python(self):
        solution = 'a = input()\nprint(a)\n'
        test = mixer.blend(
            'catalog.Test', 
            test_input='test_output', 
            test_output='test_output'
            )
        language = 'Python'

        res = additions.solution_to_file(solution, test, language)
        assert res == []

    def test_solution_to_file_ruby(self):
        solution = 'a = gets\nprint(a.chomp)\n'
        test = mixer.blend(
            'catalog.Test', 
            test_input='test_output', 
            test_output='test_output'
            )
        language = 'Ruby'

        res = additions.solution_to_file(solution, test, language)
        assert res == []

    def test_solution_testing_right_solution(self):
        user = mixer.blend('catalog.User')
        task = mixer.blend('catalog.Task')
        test = mixer.blend(
            'catalog.Test', 
            test_input='test_output', 
            test_output='test_output',
            task=task
            )
        solution = mixer.blend(
            'catalog.Solution', 
            solution='a = input()\nprint(a)\n', 
            language='Python',
            task=task,
            user=user,
            )

        additions.solution_testing(solution.id)
        solution = models.Solution.objects.get(pk=solution.id)
        user = models.User.objects.get(pk=user.id)
        assert solution.score == 1.00, 'Should evaluate to complete solution'
        assert solution.reports == '', 'Should not have reports'
        assert solution.done == True, 'Should update done status'
        assert user.user_progress == 1.00, 'Should update user progress'

    def test_solution_testing_wrong_solution(self):
        user = mixer.blend('catalog.User')
        task = mixer.blend('catalog.Task')
        test = mixer.blend(
            'catalog.Test', 
            test_input='in', 
            test_output='out',
            task=task
            )
        solution = mixer.blend(
            'catalog.Solution', 
            solution='a = input()\nprint(a)\n', 
            language='Python',
            task=task,
            user=user,
            )
 
        additions.solution_testing(solution.id)
        output = ['- i', '- n', '+ o', '+ u', '+ t']
        res = 'For test 1 diffs:' + str(output) + '\n'
        solution = models.Solution.objects.get(pk=solution.id)
        user = models.User.objects.get(pk=user.id)
        assert solution.score == 0, 'Should evaluate to wrong solution'
        assert solution.reports == res, 'Should have reports'
        assert solution.done == True, 'Should update done status'
        assert user.user_progress == 0, 'Should update user progress with 0'