from django.test import TestCase

# Create your tests here.
class NoticeboardListView(TestCase):
    def test_noticeboard_page_status(self):
        response = self.client.get('noticeboard:get_noticeboard_list')
        self.assertEqual(response.status_code, 200)
    def test_template(self):
        ...
    
    def test_comment_count(self):
        ...
        
class NoticeboardDetailView(TestCase):
    def test_detail_page_status(self):
        response = self.client.get('noticeboard:get_noticeboard_detail')
        self.assertEqual(response.status_code, 200)
    
    def test_question_template(self):
        ...
        
    def test_comment_template(self):
        ...
    
class CommentCreateView(TestCase):
    def test_comment_creation(self):
        ...
    
class UserModel(TestCase):
    def test_user_creation(self):
        ...
        
class NoticeboardModel(TestCase):
    def test_noticeboard_creation(self):
        ...
    
class CommentModel(TestCase):
    def test_comment_creation(self):
        ...