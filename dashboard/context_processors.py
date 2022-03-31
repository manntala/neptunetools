from account.models import Account

def currentusers(request):
    users = Account.objects.all()
    return dict(users=users)