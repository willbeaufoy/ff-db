from django.core.management.base import NoArgsCommand
from forum.models import Node

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for claim in Node.objects.all():
            claim.delete()