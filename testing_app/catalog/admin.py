from django.contrib import admin
from catalog.models import Task, SolutionInstance, Test, User
from django.contrib import admin

# admin.site.register(Test)
# admin.site.register(Task)
# admin.site.register(SolutionInstance)


class TestsInline(admin.TabularInline):
    model = Test


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_name', 'release_date', 'test_number')
    inlines = [TestsInline]


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('test_num', 'task', 'id')
    fields = [('test_num', 'task_id'), ("test_input", 'test_output')]


@admin.register(SolutionInstance)
class SolutionInstanceAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'score', 'attempt', 'submition_date')
    fields = [('task', 'user'), 'submition_date', 'attempt', 'solution']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'user_progress', 'date_joined', 'is_staff', 'is_active')
    fields = ['username', 'date_joined', 'password']
    list_filter = ('is_staff', 'is_active')
