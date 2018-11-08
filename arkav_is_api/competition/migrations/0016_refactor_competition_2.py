# Generated by Django 2.1.3 on 2018-11-08 09:32

from django.db import migrations


def convert_team_category_to_use_fk(apps, schema_editor):
    Team = apps.get_model('competition', 'Team')
    CompetitionCategory = apps.get_model('competition', 'CompetitionCategory')
    for team in Team.objects.all():
        try:
            team.category_fk = CompetitionCategory.objects.get(name=team.category)
            team.save()
        except CompetitionCategory.DoesNotExist:
            print(
                'WARNING: CompetitionCategory with name %s does not exist for team ID %d, name %s.' % (
                    team.category,
                    team.id,
                    team.name
                )
            )
            print('You might need to fill in the new category field manually for this team.')


def fill_invitation_full_name_and_email(apps, schema_editor):
    TeamMember = apps.get_model('competition', 'TeamMember')
    for team_member in TeamMember.objects.all():
        if team_member.has_account:
            team_member.invitation_full_name = team_member.user.full_name
            team_member.invitation_email = team_member.user.email
            team_member.save()


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0015_refactor_competition_1'),
    ]

    operations = [
        migrations.RunPython(convert_team_category_to_use_fk),
        migrations.RunPython(fill_invitation_full_name_and_email),
    ]
