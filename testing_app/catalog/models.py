from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    """Model representing a User"""
    user_progress = models.IntegerField(default=0)

    class Meta:
        ordering = ['user_progress', 'username']

    def __str__(self):
        return f'{self.id}: {self.username}'

    def get_all_tasks(self):
        solutions = [sol.id for sol in SolutionInstance.objects.all() if sol.user.id == self.id]
        return [task for task in Task.objects.all() if task.id in solutions]

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])


class Task(models.Model):
    """Model representing a Task"""
    task_name = models.CharField(max_length=64)
    release_date = models.DateField(null=True, blank=True)
    test_number = models.IntegerField(default=0)
    text = models.TextField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.id}: {self.task_name}'

    def get_absolute_url(self):
        return reverse('task-detail', args=[str(self.id)])


class Test(models.Model):
    """Model representing a Test"""
    test_num = models.IntegerField(default=1)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, null=True)
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
    task = models.ForeignKey('Task', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    score = models.IntegerField(default=0)
    attempt = models.IntegerField(default=0)
    submition_date = models.DateField(null=True, blank=True)
    solution = models.TextField()

    class Meta:
        ordering = ['submition_date', 'user']

    def __str__(self):
        """String for representing the Model object."""
        return f'SolutionInstance for task: "{self.task.task_name}", by {self.user.username}'

    def get_absolute_url(self):
        return reverse('solution-detail', args=[str(self.id)])
