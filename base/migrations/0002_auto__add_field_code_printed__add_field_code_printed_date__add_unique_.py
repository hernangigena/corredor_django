# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Code.printed'
        db.add_column(u'base_code', 'printed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Code.printed_date'
        db.add_column(u'base_code', 'printed_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding unique constraint on 'Code', fields ['code']
        db.create_unique(u'base_code', ['code'])


    def backwards(self, orm):
        # Removing unique constraint on 'Code', fields ['code']
        db.delete_unique(u'base_code', ['code'])

        # Deleting field 'Code.printed'
        db.delete_column(u'base_code', 'printed')

        # Deleting field 'Code.printed_date'
        db.delete_column(u'base_code', 'printed_date')


    models = {
        u'base.code': {
            'Meta': {'object_name': 'Code'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'printed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'printed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['base']