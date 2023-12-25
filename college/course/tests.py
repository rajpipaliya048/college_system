import os
from course.forms import CourseForm
from course.models import Course, Enrollment
from course.models import Department
from django_countries.fields import Country
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from http import HTTPStatus
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from users.models import Student


class CourseFormTest(TestCase):


    def setUp(self):
        self.department =  Department.objects.create(department_name= 'Computer Science', departmrnt_slug='cs')
    
    
    def test_valid_form(self):
        data = {
            'course_id': '99PP99',
            'course_name': 'Introduction to Computer Science',
            'course_details': 'A fundamental course in computer science.',
            'department': self.department,
            'course_img': 'image.jpg',
            'start_course': timezone.now().date(),
            'end_course': (timezone.now() + timezone.timedelta(days=30)).date(),
            'fees': 100,
            'html_input': 'Some HTML input',
        }
        form = CourseForm(data=data)
        self.assertTrue(form.is_valid())


    def test_invalid_form_course_id(self):
        data = {
            'course_id': '99P99',
            'course_name': 'Introduction to Computer Science',
            'course_details': 'A fundamental course in computer science.',
            'department': self.department,
            'course_img': 'image.jpg',
            'start_course': timezone.now().date(),
            'end_course': (timezone.now() + timezone.timedelta(days=30)).date(),
            'fees': 100,
            'html_input': 'Some HTML input',
        }
        form = CourseForm(data=data)
        self.assertTrue(form.is_valid(), 'Error: Invalid Course id')
        
        
    def test_invalid_time_in_form(self):
        data = {
            'course_id': '99PQ99',
            'course_name': 'Introduction to Computer Science',
            'course_details': 'A fundamental course in computer science.',
            'department': self.department,
            'course_img': 'image.jpg',
            'start_course': timezone.now().date(),
            'end_course': (timezone.now() - timezone.timedelta(days=30)).date(),
            'fees': 100,
            'html_input': 'Some HTML input',
        }
        form = CourseForm(data=data)
        self.assertTrue(form.is_valid(), 'Error: End course date should be greater than start course date')
        
        
    def test_normal_user_get_form(self):
        response = self.client.get("/course/create/")
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


    def test_invalid_form_course_id_with_special_character(self):
        data = {
            'course_id': '99@99',
            'course_name': 'Introduction to Computer Science',
            'course_details': 'A fundamental course in computer science.',
            'department': self.department,
            'course_img': 'image.jpg',
            'start_course': timezone.now().date(),
            'end_course': (timezone.now() + timezone.timedelta(days=30)).date(),
            'fees': 100,
            'html_input': 'Some HTML input',
        }
        form = CourseForm(data=data)
        self.assertTrue(form.is_valid(), 'Error: course id should not have any special character')
        
    def test_invalid_form_course_fees(self):
        data = {
            'course_id': '99@99',
            'course_name': 'Introduction to Computer Science',
            'course_details': 'A fundamental course in computer science.',
            'department': self.department,
            'course_img': 'image.jpg',
            'start_course': timezone.now().date(),
            'end_course': (timezone.now() + timezone.timedelta(days=30)).date(),
            'fees': 'somefees',
            'html_input': 'Some HTML input',
        }
        form = CourseForm(data=data)
        self.assertTrue(form.is_valid(), 'Error: course must be numeric')
        
    def test_invalid_form_department(self):
        data = {
            'course_id': '99@99',
            'course_name': 'Introduction to Computer Science',
            'course_details': 'A fundamental course in computer science.',
            'department': 'computer',
            'course_img': 'image.jpg',
            'start_course': timezone.now().date(),
            'end_course': (timezone.now() + timezone.timedelta(days=30)).date(),
            'fees': 'somefees',
            'html_input': 'Some HTML input',
        }
        form = CourseForm(data=data)
        self.assertTrue(form.is_valid(), 'Error: department-id should be Department instance')
        

class APITest(TestCase):
    
    def setUp(self):
        
        self.admin_user = User.objects.create_user(username='admin', password='admin', is_staff=True)
        self.user = User.objects.create_user(username='test', password='testpass', email='test@ex.com')
        self.student = Student.objects.create(user=self.user,
                                                    age=21, 
                                                    country=Country('US'), 
                                                    mobile_number='1234567890', 
                                                    gender='male', 
                                                    level_of_education='graduation')
        
        
        self.department =  Department.objects.create(department_name= 'Computer Science', departmrnt_slug='cs')
        
        self.course1 = Course.objects.create(course_id= '99PP99',
                                             course_name='Introduction to Computer Science',
                                             course_details='A fundamental course in computer science.',
                                             department=self.department,)
        self.course2 = Course.objects.create(course_id= '99PA99',
                                             course_name='Introduction to Computer',
                                             course_details='A fundamental course in computer science.',
                                             department=self.department,)        
        self.enrollment = Enrollment.objects.create(user_id=self.student, course_id=self.course1, enrollment_date=timezone.now().date(),)

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client = APIClient()
        
    
    def test_user_courses_api_without_param(self):
        self.client.force_login(self.admin_user)
        # self.client.credentials(HTTP_AUTHORIZATION=self.access_token)
        url = '/course/api/user_courses/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200, 'Error:email parameter required')
    
    
    def test_user_courses_api_with_param(self):
        self.client.force_login(self.admin_user)
        url = '/course/api/user_courses/?email=test@ex.com'
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        
        
    def test_retrieve_course(self):
        self.client.force_login(self.admin_user)
        url = f'/course/api/{self.course1.course_id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
        
    def test_delete_course(self):
        self.client.force_login(self.admin_user)
        url = f'/course/api/{self.course1.course_id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        
    def test_update_course(self):
        self.client.force_login(self.admin_user)
        url = f'/course/api/{self.course1.course_id}/'
        _data = {'course_name': 'new_name'}
        response = self.client.patch(url, data=_data, format='json')
        self.assertEqual(response.status_code, 200)
        
    def test_retrieve_courses(self):
        self.client.force_login(self.admin_user)
        url = f'/course/api/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_create_course_api(self):
        self.client.force_login(self.admin_user)
        file_path = os.path.join(settings.BASE_DIR, 'assets', 'default.jpeg')
        with open(file_path, 'rb') as file:
            valid_image_content = file.read()

        img = SimpleUploadedFile("valid_image.jpg", valid_image_content, content_type="image/jpeg")
        url = f'/course/api/'
        _data = {
            'course_id': '99GP99',
            'course_name': 'Introduction to Computer Science',
            'course_details': 'A fundamental course in computer science.',
            'department': self.department.pk,
            'course_img': img,
            'start_course': timezone.now().date(),
            'end_course': (timezone.now() + timezone.timedelta(days=30)).date(),
            'fees': 100,
            'html_input': 'Some HTML input',
        }
        response = self.client.post(url, data=_data, format='multipart')
        self.assertEqual(response.status_code, 201)
