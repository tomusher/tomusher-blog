# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Post.published_date'
        db.add_column('blog_post', 'published_date', self.gf('django.db.models.fields.DateTimeField')(default=''), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Post.published_date'
        db.delete_column('blog_post', 'published_date')


    models = {
        'blog.image': {
            'Meta': {'object_name': 'Image'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'blog.post': {
            'Meta': {'object_name': 'Post'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['blog']