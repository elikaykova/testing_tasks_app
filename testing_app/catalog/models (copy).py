from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class User(models.Model):
    """Model representing a User"""
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=64)
    reg_date = models.DateField(null=True, blank=True)
    user_progress = models.IntegerField(default=0)

    class Meta:
        ordering = ['user_progress', 'user_name']

    def __str__(self):
        return f'{self.user_id}: {self.user_name}'

    def get_all_tasks(self):
        a = [sol.task_id for sol in SolutionInstance.objects.all() if sol.user_id.user_id == self.user_id]
        return [task for task in Task.objects.all() if task in a]

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.user_id)])


class Task(models.Model):
    """Model representing a Task"""
    task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=64)
    release_date = models.DateField(null=True, blank=True)
    test_number = models.IntegerField(default=0)
    text = models.TextField()

    class Meta:
        ordering = ['task_id']

    def __str__(self):
        return f'{self.task_id}: {self.task_name}'

    def get_absolute_url(self):
        return reverse('task-detail', args=[str(self.task_id)])


class Test(models.Model):
    """Model representing a Test"""
    test_id = models.AutoField(primary_key=True)
    test_num = models.IntegerField(default=1)
    task_id = models.ForeignKey('Task', on_delete=models.CASCADE, null=True)
    test_input = models.TextField()
    test_output = models.TextField()

    class Meta:
        ordering = ['task_id', 'test_num']

    def __str__(self):
        return f'Test{self.test_num} for {self.task_id.task_name}'

    # def get_absolute_url(self):
    #     return reverse('test-detail', args=[str(self.test_id)])


class SolutionInstance(models.Model):
    """Model representing a solution"""
    task_id = models.ForeignKey('Task', on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
    score = models.IntegerField(default=0)
    attempt = models.IntegerField(default=0)
    submition_date = models.DateField(null=True, blank=True)
    solution = models.TextField()

    class Meta:
        ordering = ['submition_date', 'user_id']

    def __str__(self):
        """String for representing the Model object."""
        return f'SolutionInstance for task: "{self.task_id.task_name}", by {self.user_id.user_name}'

    def get_absolute_url(self):
        return reverse('solution-detail', args=[str(self.id)])
