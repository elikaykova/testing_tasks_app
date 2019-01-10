from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


class User(AbstractUser):
    """Model representing a User"""
    user_progress = models.FloatField(default=0)

    class Meta:
        ordering = ['user_progress', 'username']

    def __str__(self):
        return f'{self.id}: {self.username}'

    def get_all_tasks(self):
        solutions = [sol.id for sol in SolutionInstance.objects.all() if sol.user.id == self.id]
        return [task for task in Task.objects.all() if task.id in solutions]

    def get_all_solutions(self):
        return [sol for sol in SolutionInstance.objects.all() if sol.user.id == self.id]

    def get_max_score_for_task(self, task):
        solutions = self.get_all_solutions()
        sol = [sol.score for sol in solutions if sol.task == task]
        if sol:
            return max(sol)
        return 0

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])

    def update_score(self, score, task):
        max_score = self.get_max_score_for_task(task)
        if max_score < score:
            self.user_progress = self.user_progress - max_score + score
            self.user_progress = format(self.user_progress, '.2f')

    def get_tasks(self):
        return [tasks for task in self.get_all_tasks() if task in [sol_task.task for sol_task in self.get_all_solutions()]]

    # def create_user(self, username, email, password=None):
    #     self.username = username
    #     self.email = email
    #     self.date_joined = datetime.today()
    #     set_password(password)
    #     self.save()


class Task(models.Model):
    """Model representing a Task"""
    task_name = models.CharField(max_length=64)
    release_date = models.DateField(null=True, blank=True)
    test_number = models.IntegerField(default=0)
    text = models.TextField()
    publisher = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.id}: {self.task_name}'

    def get_absolute_url(self):
        return reverse('task-detail', args=[str(self.id)])

    @classmethod
    def get_all_tasks(cls):
        return ((task, str(task)) for task in Task.objects.all())


class Test(models.Model):
    """Model representing a Test"""
    test_num = models.IntegerField(default=1)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    test_input = models.TextField()
    test_output = models.TextField()

    class Meta:
        ordering = ['task_id', 'test_num']

    def __str__(self):
        return f'Test{self.test_num} for {self.task.task_name}'

    # def get_absolute_url(self):
    #     return reverse('test-detail', args=[str(self.test_id)])


class SolutionInstance(models.Model):
    """Model representing a solution"""
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    reports = models.TextField(null=True)
    attempt = models.IntegerField(default=0)
    submition_date = models.DateTimeField(null=True, blank=True)
    solution = models.TextField(null=True)
    done = models.BooleanField(default=False)

    class Meta:
        ordering = ['submition_date', 'user']

    def __str__(self):
        """String for representing the Model object."""
        return f'SolutionInstance for task: "{self.task.task_name}", by {self.user.username}'

    def get_absolute_url(self):
        return reverse('solution-detail', args=[str(self.id)])

    def get_queryset(self):
        return SolutionInstance.objects.filter(owner=self.kwargs['pk'])
