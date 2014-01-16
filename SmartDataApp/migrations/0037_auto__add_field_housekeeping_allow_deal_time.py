# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Housekeeping.allow_deal_time'
        db.add_column(u'SmartDataApp_housekeeping', 'allow_deal_time',
                      self.gf('django.db.models.fields.CharField')(max_length=250, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Housekeeping.allow_deal_time'
        db.delete_column(u'SmartDataApp_housekeeping', 'allow_deal_time')


    models = {
        u'SmartDataApp.community': {
            'Meta': {'object_name': 'Community'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'SmartDataApp.complaints': {
            'Meta': {'object_name': 'Complaints'},
            'author': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['SmartDataApp.Community']", 'null': 'True'}),
            'content': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'handler': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_worker_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pleased': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pleased_reason': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'src': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'SmartDataApp.express': {
            'Meta': {'object_name': 'Express'},
            'allowable_get_express_time': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'arrive_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['SmartDataApp.ProfileDetail']", 'null': 'True'}),
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['SmartDataApp.Community']", 'null': 'True'}),
            'get_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'handler': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_worker_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pleased': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pleased_reason': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'SmartDataApp.housekeeping': {
            'Meta': {'object_name': 'Housekeeping'},
            'allow_deal_time': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['SmartDataApp.ProfileDetail']", 'null': 'True'}),
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['SmartDataApp.Community']", 'null': 'True'}),
            'handler': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'housekeeping_item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['SmartDataApp.Housekeeping_items']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_worker_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pleased': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pleased_reason': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'SmartDataApp.housekeeping_items': {
            'Meta': {'object_name': 'Housekeeping_items'},
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['SmartDataApp.Community']", 'null': 'True'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'price_description': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'})
        },
        u'SmartDataApp.picture': {
            'Meta': {'object_name': 'Picture'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keep': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'like': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'src': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'timestamp_add': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'SmartDataApp.profiledetail': {
            'Meta': {'object_name': 'ProfileDetail'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['SmartDataApp.Community']", 'null': 'True'}),
            'device_chanel_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'null': 'True'}),
            'device_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'null': 'True'}),
            'device_user_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '100', 'null': 'True'}),
            'floor': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'gate_card': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '11', 'null': 'True'}),
            'profile': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'SmartDataApp.repair': {
            'Meta': {'object_name': 'Repair'},
            'author': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['SmartDataApp.Community']", 'null': 'True'}),
            'content': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'handler': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_worker_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pleased': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pleased_reason': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'repair_item': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'src': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'SmartDataApp.repair_item': {
            'Meta': {'object_name': 'Repair_item'},
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['SmartDataApp.Community']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['SmartDataApp']