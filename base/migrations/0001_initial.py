# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Code'
        db.create_table(u'base_code', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'base', ['Code'])


    def backwards(self, orm):
        # Deleting model 'Code'
        db.delete_table(u'base_code')


    models = {
        u'base.code': {
            'Meta': {'object_name': 'Code'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['base']