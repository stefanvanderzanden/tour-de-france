# Generated by Django 5.2.3 on 2025-06-29 17:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('races', '0004_riderforteam_photo_teamforround_order'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ParticipantTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='races.round', verbose_name='Ronde')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Gebruiker')),
            ],
            options={
                'verbose_name': 'Speelteam',
                'verbose_name_plural': 'Speelteams',
            },
        ),
        migrations.CreateModel(
            name='RiderForParticipantTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('participant_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.participantteam')),
                ('rider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='races.riderforteam')),
            ],
            options={
                'ordering': ('added_at',),
            },
        ),
        migrations.AddField(
            model_name='participantteam',
            name='riders',
            field=models.ManyToManyField(blank=True, through='games.RiderForParticipantTeam', to='races.riderforteam', verbose_name='Riders'),
        ),
        migrations.CreateModel(
            name='ScoreTableEntryForRound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(verbose_name='Positie')),
                ('score', models.IntegerField(verbose_name='Score')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='races.round', verbose_name='Ronde')),
            ],
            options={
                'verbose_name': 'Score tabel regel',
                'verbose_name_plural': 'Score tabel regels',
                'ordering': ('round', 'position'),
            },
        ),
        migrations.CreateModel(
            name='StageScoreForRider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(verbose_name='Positie')),
                ('score', models.IntegerField(verbose_name='Score')),
                ('rider', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='scores_for_stages', to='races.riderforteam', verbose_name='Renner')),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='scores_for_riders', to='races.stageday', verbose_name='Etappe')),
            ],
            options={
                'verbose_name': 'Score voor renner',
                'verbose_name_plural': 'Score voor renners',
                'ordering': ('stage__round', 'stage'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='participantteam',
            unique_together={('user', 'round')},
        ),
        migrations.CreateModel(
            name='StageScoreForParticipantTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score_for_stage', models.IntegerField(default=0, verbose_name='Totaal voor etappe')),
                ('accumulated_score', models.IntegerField(default=0, verbose_name='Geaccumuleerde score')),
                ('participant_team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='scores_for_stages', to='games.participantteam', verbose_name='Team voor deelnemer')),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='scores_for_participants', to='races.stageday', verbose_name='Etappe')),
                ('rider_stage_scores', models.ManyToManyField(blank=True, to='games.stagescoreforrider')),
            ],
            options={
                'verbose_name': 'Etappe score voor team',
                'verbose_name_plural': 'Etappe scores voor teams',
                'ordering': ('stage__round', 'stage'),
                'constraints': [models.UniqueConstraint(fields=('participant_team', 'stage'), name='unique score for participant and stage')],
            },
        ),
    ]
