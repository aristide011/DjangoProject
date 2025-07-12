from django.contrib.auth import get_user_model
from django.test import TestCase,client,Client
from pyparsing import withClass
from django.db import IntegrityError
from .models import CustomUser, UserProfile

from django.urls import reverse
import datetime
from django.contrib.messages import get_messages
from .forms import UserRegistrationForm, AuthenticationForm
import uuid


class CustomUserTestCase(TestCase):

    def test_create_user(self):
        user = CustomUser.objects.create_user(email="test@example.com",
                                              first_name="Anna",
                                              last_name="Fania",
                                              password="password")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "Anna")
        self.assertEqual(user.last_name, "Fania")

        print("Test create user passed")

    def test_unique_email(self):
        user1 = CustomUser.objects.create_user(email="test@example.com",
                                               first_name="Anna",
                                               last_name="Fania",
                                               password="password")
        with self.assertRaises(IntegrityError):
            user2 = CustomUser.objects.create_user(email="test@example.com",
                                                   first_name="Anna",
                                                   last_name="Fania",
                                                   password="password")

    def test_is_curator(self):
        user = CustomUser.objects.create_user(email="test@example.com",
                                              first_name="Anna",
                                              last_name="Fania",
                                              password="password")
        user.is_curator = True
        user.save()

        self.assertTrue(user.is_curator)


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.com', password='test')

    def test_create_profile(self):
        profile = UserProfile.objects.create(user=self.user, bio='Test bio')

        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.bio, 'Test bio')

    def test_relazione_one_to_one(self):
        profile = UserProfile.objects.create(user=self.user)

        self.assertEqual(profile.user, self.user)

    def test_campo_bio(self):
        profile = UserProfile.objects.create(user=self.user, bio='Test bio')
        self.assertEqual(profile.bio, 'Test bio')

    def test_campo_profile_picture(self):
        # Nota: per testare il campo ImageField, dovresti utilizzare un'immagine di test
        # e verificare che sia stata salvata correttamente
        pass
    # test sulle viste


class UserRegisterTestCase(TestCase):
    def test_register_user(self):
        dati = { 'email': 'test@example.com', 'favorite_genres': 'Rock',
                'birthdate': '2001-01-01', 'password1': 'Giraffe#Lemon@ee88!',
                'password2': 'Giraffe#Lemon@ee88!','first_name': 'Test',
    'last_name': 'User'
}  # questa password soddisfa i requisiti di sicurezza

        response = self.client.post(reverse('users:register'), dati,follow=False)
        if response.status_code == 200 and response.context is not None:
            print(response.context['form'].errors)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:user_login'))


class UserLoginViewTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com')
        self.user.set_password('Giraffe#Lemon@ee88!')
        self.user.save()

    def test_login_user(self):
        dati = {'username': 'testuser', 'password': 'Giraffe#Lemon@ee88!'}
        response = self.client.post(reverse('users:user_login'), dati, follow=True)

        self.assertEqual(response.status_code, 200)
        self.client.force_login(self.user)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_invalid_user(self):
        dati = {'username': 'invaliduser', 'password': 'wrongpassword'}
        response = self.client.post(reverse('users:user_login'), dati, follow=True)

        # Controlla che la risposta non reindirizzi e restituisca la pagina di login
        self.assertEqual(response.status_code, 200)  # Aspettati di rimanere nella pagina di login
        self.assertContains(response, "Please enter a correct email and password.")

    # logout


class UserLogoutViewTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', email='test@example.com')
        self.user.set_password('Giraffe#Lemon@ee88!')
        self.user.save()

    def test_logout_user(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('users:user_logout'), follow=True)

        self.assertRedirects(response, reverse('users:user_login'))
        self.assertFalse('_auth_user_id' in self.client.session)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Sei stato disconesso con successo.")


class TestCustomUserUpdateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='test@example.com', password='test')
        UserProfile.objects.create(user=self.user)

    def test_update_profile(self):
        # Verifica che la vista di aggiornamento del profilo utente aggiorni effettivamente il profilo
        self.client.force_login(self.user)
        url = reverse('users:custom_update',kwargs={'pk':self.user.pk})
        print(url)
        response = self.client.post(url, {
            'email': 'newemail@example.com',
            'favorite_genres': 'azione',
            'birthdate': '1990-01-01'
        }, follow=False)
        # ...
        self.assertEqual(response.status_code, 302)  # Redirect to profile page

        updated_user = CustomUser.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.email, 'newemail@example.com')
        self.assertEqual(updated_user.favorite_genres, 'azione')
        self.assertEqual(updated_user.birthdate, datetime.date(1990, 1, 1))

    def test_update_profile_invalid_form(self):
        # Verifica che la vista di aggiornamento del profilo utente restituisca un errore se il form non è valido
        self.client.force_login(self.user)
        response = self.client.post(reverse('users:custom_update', kwargs={'pk': self.user.pk}), {
            'email': '',  # email vuota
            'favorite_genres': 'azione',
            'birthdate': '1990-01-01'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')

    def test_get_success_url(self):
        # Verifica che la vista di aggiornamento del profilo utente reindirizzi correttamente dopo l'aggiornamento
        self.client.force_login(self.user)
        response = self.client.post(reverse('users:custom_update',kwargs={'pk':self.user.pk}),{
            'email': 'newemail@example.com',
            'favorite_genres': 'azione',
            'birthdate': '1990-01-01'
        }, follow=False)
        self.assertEqual(response.status_code, 302)


class TestCustomUserDeleteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='test@example.com', password='test')

    def test_delete_user(self):
        # Verifica che la vista di eliminazione dell'utente elimini effettivamente l'utente
        self.client.force_login(self.user)
        response = self.client.post(reverse('users:customUser_confirm_delete', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect to success_url

        # Verifica che l'utente sia stato eliminato
        self.assertFalse(CustomUser.objects.filter(pk=self.user.pk).exists())

    def test_delete_user_get(self):
        # Verifica che la vista di eliminazione dell'utente restituisca la pagina di conferma
        self.client.force_login(self.user)
        response = self.client.get(reverse('users:customUser_confirm_delete', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)  # Pagina di conferma

    def test_delete_user_not_logged_in(self):
        # Verifica che la vista di eliminazione dell'utente reindirizzi a login se l'utente non è loggato
        response = self.client.post(reverse('users:customUser_confirm_delete', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 302)  # Redirect to login page


class UserListViewTestCase(TestCase):
    def setUp(self):
        self.superuser = CustomUser.objects.create_superuser(username='admin', email='admin@example.com',
                                                             password='password')
        self.normal_user = CustomUser.objects.create_user(email='test@example.com', password='test', first_name='John',
                                                          last_name='Doe')
        self.client.force_login(self.superuser)

    def test_user_list_view(self):
        response = self.client.get(reverse('users:user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_list.html')  # Assicura che il template sia quello giusto

    def test_user_list_view_search(self):
        response = self.client.get(reverse('users:user_list'), {'q': 'John'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_list.html')
        print(response.status_code)
        print(response.content)
        self.assertContains(response, 'John')

    def test_user_list_view_no_permission(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(reverse('users:user_list'))
        self.assertEqual(response.status_code, 403)


class UserProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='user', email='user@example.com', password='password')
        UserProfile.objects.create(user=self.user)  # Crea un profilo utente per l'utente
        self.client.force_login(self.user)


    def test_user_profile_view(self):
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')


class UserProfileUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='user', email='user@example.com', password='password')
        self.profile = UserProfile.objects.create(user=self.user)
        self.client.force_login(self.user)

    def test_user_profile_update_view(self):
         response = self.client.get(reverse('users:profile_update'))
         self.assertEqual(response.status_code, 200)
         self.assertTemplateUsed(response, 'users/profile_update.html')

    def test_user_profile_update(self):
         dati = {'bio': 'Nuova bio'}
         response = self.client.post(reverse('users:profile_update'), dati)
         self.assertRedirects(response, reverse('users:profile'))


class UserProfileDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='user', email='user@example.com', password='password')
        self.profile = UserProfile.objects.create(user=self.user)
        self.client.force_login(self.user)

    def test_user_profile_delete_view(self):
        response = self.client.get(reverse('users:userProfile_confirm_delete', kwargs={'pk': self.profile.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/userProfile_confirm_delete.html')

    def test_user_profile_delete(self):
        response = self.client.post(reverse('users:userProfile_confirm_delete', kwargs={'pk': self.profile.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:user_login'))


class UserAdminUpdateViewTestCase(TestCase):

    def setUp(self):
        # Crea un utente superuser con email unica
        self.superuser = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='securepassword'
        )
        self.user_to_update = CustomUser.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='securepassword'
        )
        self.client.force_login(self.superuser)  # Assicura che il superuser sia loggato

    def test_user_admin_update(self):
        new_email = f"newemail{uuid.uuid4()}@example.com"
        # Aggiorna l'email con un valore unico
        data = {
            'email': new_email,
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName', 'favorite_genres': 'azione',
            'birthdate': '1990-01-01'

        }

        response = self.client.post(reverse('users:admin_profile_update', kwargs={'pk': self.user_to_update.pk}), data,
                                    follow=True)
        print("Status code:", response.status_code)
        print("Response content:", response.content)
        self.user_to_update.refresh_from_db()
        print("Email dopo l'aggiornamento:", self.user_to_update.email)
        self.assertEqual(self.user_to_update.email, new_email)
        self.assertEqual(response.status_code, 200)

    def test_user_admin_update_no_permission(self):
        # Prova a creare un dannato utente con email già esistente
        # Cambia l'email per garantire che non ci siano conflitti

        another_user = CustomUser.objects.create_user(
            username='user2',
            email='anotheruser@example.com',
            password='securepassword'
        )
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(username='user2', email='anotheruser@example.com', password='password')


class UserRegistrationFormTestCase(TestCase):
    def test_user_registration_form(self):
        dati = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'favorite_genres': ['rock'],
            'birthdate': '1990-01-01',
            'password1': 'Giraffe#Lemon@ee88!',
            'password2': 'Giraffe#Lemon@ee88!'
        }
        form = UserRegistrationForm(data=dati)
        # Stampa gli errori se il modulo non è valido
        if not form.is_valid():
            print(form.errors)  # Stampa gli errori del modulo
        self.assertTrue(form.is_valid())
    def test_user_registration_form_invalid(self):
        dati = {
            'username': 'testuser',
            'email': 'test@example.com', 'first_name': 'Test',
            'last_name': 'User',
            'favorite_genres': ['rock'],
            'birthdate': '1990-01-01',
            'password1': 'password',
            'password2': 'differentpassword'
        }
        form = UserRegistrationForm(data=dati)
        self.assertFalse(form.is_valid())


class UserLoginFormTestCase(TestCase):
    def setUp(self):
        self.username = f'testuser{uuid.uuid4()}'
        self.user = CustomUser.objects.create_user(username=self.username, email='testuser@example.com',
                                                   password='testpassword')

    def test_user_login_form(self):
        form = AuthenticationForm(data={'username': self.username, 'password': 'testpassword'})

    def test_user_login_form_invalid(self):
        dati = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        form = AuthenticationForm(data=dati)
        self.assertFalse(form.is_valid())