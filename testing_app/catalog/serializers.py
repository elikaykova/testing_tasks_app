from rest_framework import serializers
from catalog.models import Test, Task, SolutionInstance, User
from catalog.rq_test import rq_exec
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    absolute_url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = User
        # fields = ('username', 'password', 'first_name', 'last_name', 'email')
        fields = '__all__'
        ordering = ('username',)

    def create(self, validated_data, instance=None):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user


class SubmitUserSerializer(serializers.ModelSerializer):
    # absolute_url = serializers.URLField(source='get_absolute_url', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')
        # fields = '__all__'
        ordering = ('username',)

    def create(self, validated_data, instance=None):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.date_joined = timezone.now()
        # token, create = Token.objects.get_or_create(user=user)
        # user.token = token.key
        user.save()
        return user


class TaskSerializer(serializers.ModelSerializer):
    absolute_url = serializers.URLField(source='get_absolute_url', read_only=True)
    # publisher = UserSerializer()

    class Meta:
        model = Task
        fields = '__all__'
        ordering = ('id',)

    def create(self, validated_data):
        task = Task(**validated_data)
        task.save()
        return task

    def update(self, instance, validated_data):
        instance.task_name = validated_data.get('task_name', instance.task_name)
        instance.release_date = validated_data.get('release_date', instance.release_date)
        instance.text = validated_data.get('text', instance.text)
        instance.publisher = validated_data.get('publisher', instance.publisher)
        instance.save()
        return instance


class SubmitTaskSerializer(serializers.ModelSerializer):
    # absolute_url = serializers.URLField(source='get_absolute_url', read_only=True)
    # publisher = UserSerializer()

    class Meta:
        model = Task
        fields = ('task_name', 'text')

    def create(self, validated_data):
        task = Task(**validated_data)
        task.release_date = timezone.now()
        task.publisher = self.context['user']
        task.save()
        return task

    def update(self, instance, validated_data):
        instance.task_name = validated_data.get('task_name', instance.task_name)
        instance.release_date = timezone.now()
        instance.text = validated_data.get('text', instance.text)
        instance.publisher = self.context['user']
        instance.save()
        return instance


class TestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = '__all__'
        ordering = ('id',)
        # list_serializer_class = TestListSerializer


class SolutionInstanceSerializer(serializers.ModelSerializer):
    absolute_url = serializers.URLField(source='get_absolute_url', read_only=True)
    # task = TaskSerializer()
    # user = UserSerializer()

    class Meta:
        model = SolutionInstance
        fields = '__all__'
        ordering = ('id',)
        # fields = ('task', 'user', 'score', 'reports', 'submition_date', 'solution', 'absolute_url')
    
    def create(self, validated_data):
        solution = SolutionInstance(**validated_data)
        solution.save()
        print(solution)
        return solution

    def update(self, instance, validated_data):
        # instance.task = validated_data.get('task', instance.task)
        instance.submition_date = validated_data.get('submition_date', instance.submition_date)
        instance.user = validated_data.get('user', instance.user)
        instance.reports = validated_data.get('reports', instance.reports)
        instance.solution = validated_data.get('solution', instance.solution)
        instance.done = validated_data.get('done', instance.done)
        instance.save()
        return instance

class SubmitSolutionSerializer(serializers.ModelSerializer):
    absolute_url = serializers.URLField(source='get_absolute_url', read_only=True)
    # task = TaskSerializer()
    # user = UserSerializer()

    class Meta:
        model = SolutionInstance
        fields = ('solution', 'absolute_url')
        ordering = ('id',)
    
    def create(self, validated_data):
        solution = SolutionInstance(**validated_data)
        solution.task = self.context['task']
        solution.user = self.context['user']
        solution.submition_date = self.context['date']
        solution.save()
        print(solution.id)
        rq_exec(solution.id)
        return solution

    # def update(self, instance, validated_data):
    #     instance.task = validated_data.get('task', instance.task)
    #     instance.submition_date = validated_data.get('submition_date', instance.submition_date)
    #     instance.user = validated_data.get('user', instance.user)
    #     instance.reports = validated_data.get('reports', instance.reports)
    #     instance.solution = validated_data.get('solution', instance.solution)
    #     instance.done = validated_data.get('done', instance.done)
    #     instance.save()
    #     return instance
