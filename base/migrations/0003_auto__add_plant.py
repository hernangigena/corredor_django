# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Plant'
        db.create_table(u'base_plant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['base.Code'], unique=True)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=17)),
            ('lng', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=17)),
        ))
        db.send_create_signal(u'base', ['Plant'])


    def backwards(self, orm):
        # Deleting model 'Plant'
        db.delete_table(u'base_plant')


    models = {
        u'base.code': {
            'Meta': {'object_name': 'Code'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'printed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'printed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'base.plant': {
            'Meta': {'object_name': 'Plant'},
            'code': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['base.Code']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '17'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '17'})
        }
    }

    complete_apps = ['base']