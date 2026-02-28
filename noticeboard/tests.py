from django.test import TestCase
from django.urls import reverse
from .models import User, Noticeboard, Comment

class NoticeboardListViewTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create(username='testuser')

        # Create test notices
        self.notice1 = Noticeboard.objects.create(
            title='Test Notice 1',
            content='Test content 1',
            author=self.user
        )
        self.notice2 = Noticeboard.objects.create(
            title='Test Notice 2',
            content='Test content 2',
            author=self.user
        )

        # Create test comments
        Comment.objects.create(
            content='Test comment 1',
            author=self.user,
            noticeboard=self.notice1
        )
        Comment.objects.create(
            content='Test comment 2',
            author=self.user,
            noticeboard=self.notice1
        )

    def test_noticeboard_page_status(self):
        response = self.client.get(reverse('noticeboard:noticeboard_list'))
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(reverse('noticeboard:noticeboard_list'))
        self.assertTemplateUsed(response, 'noticeboardList.html')

    def test_comment_count(self):
        response = self.client.get(reverse('noticeboard:noticeboard_list'))
        notices = response.context['notices']

        # Find our test notice in the context
        notice_with_comments = None
        for notice in notices:
            if notice.pk == self.notice1.pk:
                notice_with_comments = notice
                break

        self.assertIsNotNone(notice_with_comments)
        self.assertEqual(notice_with_comments.comments_count, 2)

class NoticeboardDetailViewTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create(username='testuser')

        # Create test notice
        self.notice = Noticeboard.objects.create(
            title='Test Notice',
            content='Test content',
            author=self.user
        )

        # Create test comments
        self.comment1 = Comment.objects.create(
            content='Test comment 1',
            author=self.user,
            noticeboard=self.notice
        )
        self.comment2 = Comment.objects.create(
            content='Test comment 2',
            author=self.user,
            noticeboard=self.notice
        )

    def test_detail_page_status(self):
        response = self.client.get(reverse('noticeboard:noticeboard_detail', args=[self.notice.pk]))
        self.assertEqual(response.status_code, 200)

    def test_question_template(self):
        response = self.client.get(reverse('noticeboard:noticeboard_detail', args=[self.notice.pk]))
        self.assertTemplateUsed(response, 'noticeboardDetail.html')

    def test_comment_template(self):
        response = self.client.get(reverse('noticeboard:noticeboard_detail', args=[self.notice.pk]))
        comments = response.context['comments']
        self.assertEqual(len(comments), 2)
        self.assertIn(self.comment1, comments)
        self.assertIn(self.comment2, comments)

class CommentCreateViewTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create(username='testuser')

        # Create test notice
        self.notice = Noticeboard.objects.create(
            title='Test Notice',
            content='Test content',
            author=self.user
        )

    def test_comment_creation(self):
        # Test POST request to create comment
        response = self.client.post(
            reverse('noticeboard:create_comment', args=[self.notice.pk]),
            {
                'content': 'Test comment content',
                'author': 'testuser'
            }
        )

        # Check redirect response
        self.assertEqual(response.status_code, 302)

        # Check comment was created
        comments = Comment.objects.all()
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].content, 'Test comment content')
        self.assertEqual(comments[0].author.username, 'Testuser')  # Capitalized
        self.assertEqual(comments[0].noticeboard, self.notice)

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create(username='testuser')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(User.objects.filter(username='testuser').exists())

class NoticeboardModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')

    def test_noticeboard_creation(self):
        notice = Noticeboard.objects.create(
            title='Test Notice',
            content='Test content',
            author=self.user
        )
        self.assertEqual(notice.title, 'Test Notice')
        self.assertEqual(notice.content, 'Test content')
        self.assertEqual(notice.author, self.user)
        self.assertTrue(Noticeboard.objects.filter(title='Test Notice').exists())

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.notice = Noticeboard.objects.create(
            title='Test Notice',
            content='Test content',
            author=self.user
        )

    def test_comment_creation(self):
        comment = Comment.objects.create(
            content='Test comment',
            author=self.user,
            noticeboard=self.notice
        )
        self.assertEqual(comment.content, 'Test comment')
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.noticeboard, self.notice)
        self.assertTrue(Comment.objects.filter(content='Test comment').exists())