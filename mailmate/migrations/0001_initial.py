# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Email'
        db.create_table(u'mailmate_email', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('from_email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'mailmate', ['Email'])

        # Adding model 'Receiver'
        db.create_table(u'mailmate_receiver', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.related.ForeignKey')(related_name='receivers', to=orm['mailmate.Email'])),
            ('address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'mailmate', ['Receiver'])


    def backwards(self, orm):
        # Deleting model 'Email'
        db.delete_table(u'mailmate_email')

        # Deleting model 'Receiver'
        db.delete_table(u'mailmate_receiver')


    models = {
        u'mailmate.email': {
            'Meta': {'object_name': 'Email'},
            'email_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'from_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'mailmate.receiver': {
            'Meta': {'object_name': 'Receiver'},
            'address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'email': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receivers'", 'to': u"orm['mailmate.Email']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['mailmate']