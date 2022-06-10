from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import  Post

# Create your tests here.

class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        # Post가 있는 경우
        self.assertEqual(Post.objects.count(), 0)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        #self.assertEqual(soup.title.text, 'Blog App')

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        logo_btn = navbar.find('a', text='Django Blog App')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(logo_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(logo_btn.attrs['href'], '/blog/')


    # def test_post_detail(self):
    #      post_000 = Post.object.create(title='테스트입니다')
    #      self.assertEqual(post_000.get_absolute_url(), '/blog/1')
