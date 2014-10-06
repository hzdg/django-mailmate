# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

        for receiver in orm['mailmate.receiver'].objects.all():
            user = orm['mailmate.user'].objects.filter(
                address=receiver.address).first()
            if not user:
                receiver.email.users.create(address=receiver.address)
            else:
                receiver.email.users.add(user)

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'mailmate.email': {
            'Meta': {'object_name': 'Email'},
            'email_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'from_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_testing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['mailmate.User']", 'symmetrical': 'False'})
        },
        u'mailmate.receiver': {
            'Meta': {'object_name': 'Receiver'},
            'address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'email': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receivers'", 'to': u"orm['mailmate.Email']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'mailmate.user': {
            'Meta': {'ordering': "('-is_test_user',)", 'object_name': 'User'},
            'address': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_test_user': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['mailmate']
    symmetrical = True
