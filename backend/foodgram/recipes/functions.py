from django.contrib.auth import get_user_model

User = get_user_model()


def get_or_create_deleted_user():
    deleted_user, created = User.objects.get_or_create(
        first_name='DELETED_USER',
        last_name='DELETED_USER',
        username='DELETED_USER',
        email='DELETED@USER.COM',
    )
    if created:
        deleted_user = User.objects.get(username='DELETED_USER')
    return deleted_user.id
