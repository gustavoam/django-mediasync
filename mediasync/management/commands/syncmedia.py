from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from mediasync.conf import msettings
import mediasync

class Command(BaseCommand):

    help = "Sync local media with remote client"
    args = '[options]'

    requires_model_validation = False

    def add_arguments(self, parser):
        parser.add_argument(
            '-F', '--force',
            dest='force',
            action='store_true',
            default=False,
            help='force files to sync',

        )

    def handle(self, *args, **options):

        msettings['SERVE_REMOTE'] = True

        force = options.get('force') or False

        try:
            mediasync.sync(force=force)
        except ValueError, ve:
            raise CommandError('%s\nUsage is mediasync %s' % (ve.message, self.args))
