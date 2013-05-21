# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UrlQRCode'
        db.create_table(u'base_urlqrcode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('qr_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('qr_image_height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('qr_image_width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'base', ['UrlQRCode'])

        # Adding field 'Code.qr_code'
        db.add_column(u'base_code', 'qr_code',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.UrlQRCode'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'UrlQRCode'
        db.delete_table(u'base_urlqrcode')

        # Deleting field 'Code.qr_code'
        db.delete_column(u'base_code', 'qr_code_id')


    models = {
        u'base.code': {
            'Meta': {'object_name': 'Code'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'printed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'printed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'qr_code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['base.UrlQRCode']", 'null': 'True'})
        },
        u'base.urlqrcode': {
            'Meta': {'object_name': 'UrlQRCode'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'qr_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'qr_image_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'qr_image_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['base']