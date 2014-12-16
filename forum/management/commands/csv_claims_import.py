from django.core.management.base import BaseCommand, NoArgsCommand, CommandError
from forum.models import *
from forum.actions import *
# from forum.utils import html
import csv
from django.utils.safestring import mark_safe




# class Command(NoArgsCommand):
#     def handle_noargs(self, **options):
#         objs = Comment.objects.all()
#         print objs

#         # Load csv file from parameter

#         infile = 

#         # Save lines of csv file as new questions

#         for line in infile:
#             q = Question(title = qtitle, tagnames = tags, author_id = author, body = qbody)
#             q.save()

class Command(BaseCommand):
    args = '<path_to_filename.csv>'
    help = 'Imports claims csv file to database'
    # Load csv file from parameter

    def handle(self, *args, **options):
        print(args[0])
        import sys
        sys.path.append('/home/will/venvs/ffosqa/ffosqa/forum/markdownext')
        print(sys.path)
        infile = args[0]
        with open(infile, 'rb') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                print row
                title = row['Quote'][:300]
                username = row['Claim ID']
                print(username)
                qbody = "Claim: {claim}\nNotes e.g. correction: {notes}\nSource: {source}\n".format(claim=row['Claim'], notes=row['Notes e.g. correction'], source=row['Where, e.g. Telegraph'])
                # qbody = 'this is the body'
                print qbody
                if username is '':
                    print('isnone')
                    u_id = User.objects.get(username='Anonymous').pk
                else:
                    print('isnotnone')
                    if User.objects.filter(username=username).exists():
                        u_id = User.objects.get(username=username).pk
                    else:
                        print('unotfound')
                        # create anon user and add as this
                        email = 'placeholder@placeholder.com'
                        password = 'fullfact'
                        u = User(username=username, email=email, is_approved=True, email_isvalid=True, real_name=row['Claim ID'])
                        u.set_password(password)
                        u.save()
                        u_id = User.objects.get(username=username).pk
                # Save lines of csv file as new questions
                q = Question(title = title, tagnames = '', author_id = u_id, body = qbody)
                q.save()