
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
from django.conf import settings




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Gli utenti devono avere un indirizzo email.')
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):  # modello personalizzato per gli utenti
    is_curator = models.BooleanField(default=False)  # Per indicare se un utente ha il ruolo di curatore o meno
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True,blank=False,null=False)
    favorite_genres = models.CharField(max_length=100)
    birthdate = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()  # Specifica il gestore

    def __str__(self):
        return f"{self.first_name}{self.last_name} {self.last_name} ({self.email})"

    groups = models.ManyToManyField(

        'auth.Group',
        related_name='customUser_set',
        blank=True,
        help_text='The groups this user belong to. ',
        verbose_name='groups')

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customer_permission',
        blank=True,
        help_text='The permissions this user has.',
        verbose_name='permissions'

    )


class UserProfile(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    bio=models.TextField(blank=True)
    profile_picture=models.ImageField(upload_to='profile_pictures', blank=True)

    def __str__(self):
        return f"profilo di {self.user.first_name}{self.user.last_name}({self.user.email})"
