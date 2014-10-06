# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'mailmate_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('is_test_user', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'mailmate', ['User'])

        # Adding field 'Email.is_enabled'
        db.add_column(u'mailmate_email', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Email.is_testing'
        db.add_column(u'mailmate_email', 'is_testing',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding M2M table for field users on 'Email'
        m2m_table_name = db.shorten_name(u'mailmate_email_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('email', models.ForeignKey(orm[u'mailmate.email'], null=False)),
            ('user', models.ForeignKey(orm[u'mailmate.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['email_id', 'user_id'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'mailmate_user')

        # Deleting field 'Email.is_enabled'
        db.delete_column(u'mailmate_email', 'is_enabled')

        # Deleting field 'Email.is_testing'
        db.delete_column(u'mailmate_email', 'is_testing')

        # Removing M2M table for field users on 'Email'
        db.delete_table(db.shorten_name(u'mailmate_email_users'))


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