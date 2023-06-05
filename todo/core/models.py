from django.db import models

# Create your models here.
class Todo(models.Model):
    id = models.AutoField(db_column='task_id', primary_key=True)
    name = models.CharField(null=True, max_length=200)
    description = models.CharField(null=True, max_length=200)
    due_date = models.DateField()
    repeat = models.CharField(2, null=False)
    completed = models.SmallIntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    deleted = models.SmallIntegerField(default=0)

    class Meta(object):
        db_table = 'task'