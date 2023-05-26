from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# from movies.models import Movie


#  Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, password2=None):
        """
        Creates and saves a User with the given email and name password.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email and name password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

#  Custom User Model


class User(AbstractBaseUser):
    ADMIN = 'Admin'
    STAFF = 'Staff'
    USER = 'User'

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (STAFF, 'Staff'),
        (USER, 'User')
    )

    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=20,
                            choices=ROLE_CHOICES, blank=True, null=True, default=USER)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Profile(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=6, choices=GENDER)
    dob = models.DateField(auto_now=False, auto_now_add=False)
    country = models.CharField(max_length=255)
    number = models.CharField(max_length=15)
    avatar = models.ImageField(upload_to='UserProfile/', blank=True)


    def __str__(self):
        return self.user.name


class Wishlist(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_wishlist')
    to_wishlist = models.ManyToManyField(
        'venues.Venue', related_name='towishlist', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email 


# class UserList(models.Model):
#     LIST_TYPE = (
#         ('Movies', 'Movies'),
#         ('People', 'People'),
#     )
#     user = models.OneToOneField(
#         User, on_delete=models.CASCADE, related_name='user_list')
#     list_title = models.CharField(max_length=255)
#     list_description = models.TextField(blank=True)
#     list_type = models.CharField(max_length=6, choices=LIST_TYPE)
#     movies_list = models.ManyToManyField(
#         'movies.Movie', related_name='movies_list', blank=True)
#     celebrity_list = models.ManyToManyField(
#         'actor.Celebrity', related_name='celebrities_list', blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.user.name + '/' + self.list_title
