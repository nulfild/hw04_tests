from django.test import TestCase, Client
from django.urls import reverse

from ..models import Post, User


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        Post.objects.create(
            text='Текстовый пост',
            author=cls.user
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_creating_post(self):
        """Новый пост добавляется в БД."""
        posts_count = Post.objects.count()

        form_data = {
            'text': 'Тестируем опять',
            'author': self.user
        }

        self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_editing_post(self):
        """Пост имзенется в БД при его редактировании."""
        form_data = {
            'text': 'Тестируем не опять, а снова',
            'author': self.user
        }
        self.authorized_client.post(
            reverse('posts:post_edit', args=('1',)),
            data=form_data,
            follow=True
        )
        self.assertEqual(
            Post.objects.get(pk=1).text, 'Тестируем не опять, а снова'
        )
