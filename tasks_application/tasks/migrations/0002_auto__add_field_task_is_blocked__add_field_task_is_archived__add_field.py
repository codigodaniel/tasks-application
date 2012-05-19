# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Task.is_blocked'
        db.add_column('tasks_task', 'is_blocked', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Task.is_archived'
        db.add_column('tasks_task', 'is_archived', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Task.is_closed'
        db.add_column('tasks_task', 'is_closed', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Task.size'
        db.add_column('tasks_task', 'size', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Task.is_blocked'
        db.delete_column('tasks_task', 'is_blocked')

        # Deleting field 'Task.is_archived'
        db.delete_column('tasks_task', 'is_archived')

        # Deleting field 'Task.is_closed'
        db.delete_column('tasks_task', 'is_closed')

        # Deleting field 'Task.size'
        db.delete_column('tasks_task', 'size')


    models = {
        'tasks.task': {
            'Meta': {'object_name': 'Task'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_blocked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['tasks']
