# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Author'
        db.create_table('stats_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author_string', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('aliases', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('stats', ['Author'])


    def backwards(self, orm):
        
        # Deleting model 'Author'
        db.delete_table('stats_author')


    models = {
        'stats.author': {
            'Meta': {'object_name': 'Author'},
            'aliases': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'author_string': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'stats.repository': {
            'Meta': {'ordering': "['name']", 'object_name': 'Repository'},
            'autobuild': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'built': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'repourl': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['stats']
