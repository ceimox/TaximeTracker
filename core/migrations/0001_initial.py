# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'core_userprofile', (
            (u'user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'core', ['UserProfile'])

        # Adding model 'Project'
        db.create_table(u'core_project', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, primary_key=True)),
            ('price_per_hour', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'core', ['Project'])

        # Adding model 'Task'
        db.create_table(u'core_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=200, null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.UserProfile'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Project'], null=True)),
            ('started', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'core', ['Task'])

        # Adding model 'Timer'
        db.create_table(u'core_timer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('initial_time', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('final_time', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Task'], null=True)),
        ))
        db.send_create_signal(u'core', ['Timer'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'core_userprofile')

        # Deleting model 'Project'
        db.delete_table(u'core_project')

        # Deleting model 'Task'
        db.delete_table(u'core_task')

        # Deleting model 'Timer'
        db.delete_table(u'core_timer')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.project': {
            'Meta': {'object_name': 'Project'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True'}),
            'price_per_hour': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core.task': {
            'Meta': {'object_name': 'Task'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Project']", 'null': 'True'}),
            'started': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.UserProfile']"})
        },
        u'core.timer': {
            'Meta': {'object_name': 'Timer'},
            'final_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Task']", 'null': 'True'})
        },
        u'core.userprofile': {
            'Meta': {'object_name': 'UserProfile', '_ormbases': [u'auth.User']},
            u'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['core']