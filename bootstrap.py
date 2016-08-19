# From https://docs.sentry.io/on-premise/server/faq/
# Only run on a fresh install with a fresh database

# docker run --rm -it --env-file=/etc/sentry.conf -e BOOTSTRAP_ORG_NAME=myvalue \
# -e BOOTSTRAP_TEAM_NAME=myvalue \
# -e BOOTSTRAP_PROJECT_NAME=myvalue \
# -e BOOTSTRAP_ADMIN_USERNAME=myvalue \
# -e BOOTSTRAP_ADMIN_PASSWORD=myvalue \
# -e BOOTSTRAP_ADMIN_EMAIL=myvalue \
# jumpcloud/sentry python bootstrap.py

# Bootstrap the Sentry environment
from sentry.utils.runner import configure
configure()

# Do something crazy
from sentry.models import ( # noqa
    Team, Project, ProjectKey, User, Organization, OrganizationMember,
    OrganizationMemberTeam
)

import os # noqa
org_name = os.env.get("BOOTSTRAP_ORG_NAME", None)
team_name = os.env.get("BOOTSTRAP_TEAM_NAME", None)
project_name = os.env.get("BOOTSTRAP_PROJECT_NAME", None)

admin_user = os.env.get("BOOTSTRAP_ADMIN_USERNAME", None)
admin_pass = os.env.get("BOOTSTRAP_ADMIN_PASSWORD", None)
admin_email = os.env.get("BOOTSTRAP_ADMIN_EMAIL", None)

organization = Organization()
organization.name = org_name
organization.save()

team = Team()
team.name = team_name
team.organization = organization
team.save()

project = Project()
project.team = team
project.name = project_name
project.organization = organization
project.save()

user = User()
user.username = admin_user
user.email = admin_email
user.is_superuser = True
user.set_password(admin_pass)
user.save()

member = OrganizationMember.objects.create(
    organization=organization,
    user=user,
    role='owner',
)

OrganizationMemberTeam.objects.create(
    organizationmember=member,
    team=team,
)

key = ProjectKey.objects.filter(project=project)[0]
print('SENTRY_DSN = "%s"' % (key.get_dsn(),))
