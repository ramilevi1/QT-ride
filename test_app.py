from unittest.mock import patch, Mock
import unittest
from app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    @patch('app.render_template')
    def test_index_route(self, mock_render_template):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        mock_render_template.assert_called_with('index.html', title='QT-Ride') 

    @patch('app.render_template')
    def test_blog_route(self, mock_render_template):
        with patch('app.BlogPost') as mock_blogpost:
            # Mocking the query method of BlogPost
            mock_query = mock_blogpost.query
            # Mocking the paginate method of the query
            mock_paginate = mock_query.order_by.return_value.paginate
            mock_paginate.return_value.items = [
                Mock(id=1, title='Post 1', content='Content of post 1'),
                Mock(id=2, title='Post 2', content='Content of post 2'),
                # Add more mock blog posts as needed
            ]
            response = self.app.get('/blog')
            self.assertEqual(response.status_code, 200)

        
    @patch('app.render_template')
    def test_contactus_route(self, mock_render_template):
        response = self.app.get('/contactus')
        self.assertEqual(response.status_code, 200)
        mock_render_template.assert_called_with('contactus.html', title="QT-ride")

    
    @patch('app.db.session.query')
    @patch('app.render_template')
    def test_search_without_query(self, mock_render_template, mock_query):
    # Define the mock data for the database query
        mock_data = [{}]
        # Mock the database query to return the mock data
        mock_query.return_value.filter.return_value.paginate.return_value.items = mock_data
    
        # Call the search route handler function
        with app.test_request_context('/search?query='):
          search_route_handler()
        # Assert that render_template is called with the correct arguments
        mock_render_template.assert_called_once_with("blog.html", blog_posts=mock_data)
    

    @patch('app.db.session.query')
    @patch('app.render_template')
    def test_search_with_query(self, mock_render_template, mock_query):
    # Define the mock data for the database query
    
        mock_data = [
            {'title': 'Post 1', 'content': 'Content of Post 1'},  # Simulated blog post 1
            {'title': 'Post 2', 'content': 'Content of Post 2'},  # Simulated blog post 2
            {'title': 'Post 3', 'content': 'Content of Post 3'}   # Simulated blog post 3
        ]
    
    # Mock the database query to return the mock data
        mock_query.return_value.filter.return_value.paginate.return_value.items = mock_data
    
    # Call the search route handler function
        with app.test_request_context('/search?query=test'):
         search_route_handler()

    # Assert that render_template is called with the correct arguments
        mock_render_template.assert_called_once_with("blog.html", blog_posts=mock_data)


if __name__ == '__main__':
    unittest.main()
