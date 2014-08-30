# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Renner'
        db.create_table(u'game_renner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('naam', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('nummer', self.gf('django.db.models.fields.IntegerField')()),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='renner_team', to=orm['game.Team'])),
        ))
        db.send_create_signal(u'game', ['Renner'])

        # Adding model 'Team'
        db.create_table(u'game_team', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('naam', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'game', ['Team'])

        # Adding model 'Etappe'
        db.create_table(u'game_etappe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nummer', self.gf('django.db.models.fields.IntegerField')()),
            ('start', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('einde', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'game', ['Etappe'])


    def backwards(self, orm):
        # Deleting model 'Renner'
        db.delete_table(u'game_renner')

        # Deleting model 'Team'
        db.delete_table(u'game_team')

        # Deleting model 'Etappe'
        db.delete_table(u'game_etappe')


    models = {
        u'game.etappe': {
            'Meta': {'object_name': 'Etappe'},
            'einde': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nummer': ('django.db.models.fields.IntegerField', [], {}),
            'start': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'game.renner': {
            'Meta': {'object_name': 'Renner'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'naam': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'nummer': ('django.db.models.fields.IntegerField', [], {}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'renner_team'", 'to': u"orm['game.Team']"})
        },
        u'game.team': {
            'Meta': {'object_name': 'Team'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'naam': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['game']