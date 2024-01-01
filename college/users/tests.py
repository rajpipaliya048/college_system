from django_countries.fields import Country
from django.contrib.auth.models import User
from django.test import TestCase
from users.forms import StudentForm

# class UserRegisterViewsTest(TestCase):
    
#     def setUp(self):
#         pass
    
#     def tesst_user_register(self):
#         _data = {
#             "email" : 'test@example.com',
#             'username' : 'test',
#             'password' : 'somerandom@12345678',
#         }
#         request = self.client.post('/signup/', data=_data)
#         response = self.client.get('/signup/')
#         self.assertEqual(response.status_code, 200)


class StudentFormTest(TestCase):
        
            
    def test_valid_form(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'somerandom@12345678',
            'password2': 'somerandom@12345678',
            'age': 21,
            'country': Country('US'),
            'mobile_number': '1234567890',
            'gender': 'male',
            'level_of_education': 'graduation',
        }
        form = StudentForm(data=data)
        self.assertTrue(form.is_valid())
        
        
    def test_invalid_username(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser@#',
            'email': 'test@example.com',
            'password1': 'somerandom@12345678',
            'password2': 'somerandom@12345678',
            'age': 21,
            'country': Country('US'),
            'mobile_number': '1234567890',
            'gender': 'male',
            'level_of_education': 'graduation',
        }
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())
        
    def test_invalid_email(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'email': 'testple.com',
            'password1': 'somerandom@12345678',
            'password2': 'somerandom@12345678',
            'age': 21,
            'country': Country('US'),
            'mobile_number': '1234567890',
            'gender': 'male',
            'level_of_education': 'graduation',
        }
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())
        
    def test_invalid_password(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'somerandom@12345678',
            'password2': 'somerandom12345678',
            'age': 21,
            'country': Country('US'),
            'mobile_number': '1234567890',
            'gender': 'male',
            'level_of_education': 'graduation',
        }
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())
        
    def test_invalid_age(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'somerandom@12345678',
            'password2': 'somerandom@12345678',
            'age': -21,
            'country': Country('US'),
            'mobile_number': '1234567890',
            'gender': 'male',
            'level_of_education': 'graduation',
        }
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())
        
    
    def test_invalid_mobile_number(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'somerandom@12345678',
            'password2': 'somerandom@12345678',
            'age': 21,
            'country': Country('US'),
            'mobile_number': 'number',
            'gender': 'male',
            'level_of_education': 'graduation',
        }
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())