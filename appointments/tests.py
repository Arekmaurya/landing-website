import json
import os
from unittest.mock import patch, MagicMock

from django.test import TestCase, Client


class HomepageTests(TestCase):
    """Test the main landing page loads and renders correctly."""

    def setUp(self):
        self.client = Client()

    def test_homepage_returns_200(self):
        """Homepage should return HTTP 200."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_contains_doctor_name(self):
        """Homepage should display the doctor's name."""
        response = self.client.get('/')
        self.assertContains(response, 'Dr. Akhil Agnihotri')

    def test_homepage_contains_nav_links(self):
        """Homepage should have all navigation links."""
        response = self.client.get('/')
        self.assertContains(response, 'href="#home"')
        self.assertContains(response, 'href="#about"')
        self.assertContains(response, 'href="#specialties"')
        self.assertContains(response, 'href="#testimonials"')
        self.assertContains(response, 'href="#contact"')

    def test_homepage_contains_appointment_form(self):
        """Homepage should have the appointment booking form."""
        response = self.client.get('/')
        self.assertContains(response, 'id="appointment-form"')
        self.assertContains(response, 'id="name"')
        self.assertContains(response, 'id="age"')
        self.assertContains(response, 'id="sex"')
        self.assertContains(response, 'id="contact"')
        self.assertContains(response, 'id="submit-btn"')

    def test_homepage_contains_hero_section(self):
        """Homepage should have the hero section."""
        response = self.client.get('/')
        self.assertContains(response, 'Move Freely, Live Fully.')

    def test_homepage_contains_specialties_section(self):
        """Homepage should have the specialties section."""
        response = self.client.get('/')
        self.assertContains(response, 'Clinical Specialties')
        self.assertContains(response, 'Knee & Hip Restoration')
        self.assertContains(response, 'Shoulder Arthroscopy')

    def test_homepage_contains_footer(self):
        """Homepage should have the footer."""
        response = self.client.get('/')
        self.assertContains(response, 'Orthocare.')
        self.assertContains(response, '2026 Orthocare Specialist')


class CredentialsTests(TestCase):
    """Test that credentials are loaded from JSON and rendered."""

    def setUp(self):
        self.client = Client()

    def test_credentials_rendered_from_json(self):
        """Credentials from credentials.json should appear on the page."""
        response = self.client.get('/')
        self.assertContains(response, 'Board-Certified Orthopaedic Surgeon')
        self.assertContains(response, 'Fellowship Trained in Sports Medicine')
        self.assertContains(response, 'Member of the National Orthopaedic Association')

    def test_credentials_json_is_valid(self):
        """credentials.json should be valid JSON and a list of strings."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, 'data', 'credentials.json')
        with open(path, 'r') as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)
        for item in data:
            self.assertIsInstance(item, str)


class ReviewsTests(TestCase):
    """Test that reviews are loaded from JSON and rendered."""

    def setUp(self):
        self.client = Client()

    def test_reviews_rendered_from_json(self):
        """Reviews from reviews.json should appear on the page."""
        response = self.client.get('/')
        self.assertContains(response, 'Michael S.')
        self.assertContains(response, 'Jessica R.')
        self.assertContains(response, 'David T.')

    def test_reviews_json_is_valid(self):
        """reviews.json should be valid JSON with required fields."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, 'data', 'reviews.json')
        with open(path, 'r') as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)
        for review in data:
            self.assertIn('quote', review)
            self.assertIn('initial', review)
            self.assertIn('name', review)
            self.assertIn('stars', review)
            self.assertIsInstance(review['stars'], int)
            self.assertTrue(1 <= review['stars'] <= 5)

    def test_star_ratings_render(self):
        """Star icons should render for reviews."""
        response = self.client.get('/')
        self.assertContains(response, 'fa-solid fa-star')


class ConfigTests(TestCase):
    """Test that config.json is valid and contains expected keys."""

    def test_config_json_is_valid(self):
        """config.json should be valid JSON with notification_method."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, 'data', 'config.json')
        with open(path, 'r') as f:
            data = json.load(f)
        self.assertIn('notification_method', data)
        self.assertIn(data['notification_method'], ['email', 'whatsapp', 'both'])


class ContactTests(TestCase):
    """Test contact details and maps embed loading/resolution."""

    def setUp(self):
        self.client = Client()

    def test_contact_json_is_valid(self):
        """contact.json should be valid JSON and have required fields."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, 'data', 'contact.json')
        with open(path, 'r') as f:
            data = json.load(f)
        self.assertIn('address', data)
        self.assertIn('phone', data)
        self.assertIn('whatsapp', data)
        self.assertIn('working_hours', data)
        self.assertIn('map_link', data)

    def test_contact_rendered_on_homepage(self):
        """Contact info from contact.json should appear on the homepage."""
        response = self.client.get('/')
        self.assertContains(response, '123 Medical Arcade')
        self.assertContains(response, '+1 (555) 123-4567')

    def test_resolve_map_embed_url(self):
        """Test the resolve_map_embed_url helper logic."""
        from appointments.views import resolve_map_embed_url
        
        # 1. Custom embed URL already formatted
        url = "https://www.google.com/maps/embed?pb=123"
        self.assertEqual(resolve_map_embed_url(url), url)
        
        # 2. Plain address name
        addr = "1600 Amphitheatre Pkwy, Mountain View, CA"
        resolved = resolve_map_embed_url(addr)
        self.assertIn("q=1600%20Amphitheatre%20Pkwy", resolved)
        self.assertIn("output=embed", resolved)
        
        # 3. Share URL with place parameter
        share_url = "https://www.google.com/maps/place/Empire+State+Building/@40.7484405,-73.9882393,17z"
        resolved_share = resolve_map_embed_url(share_url)
        self.assertIn("q=Empire+State+Building", resolved_share)
        self.assertIn("output=embed", resolved_share)


class AppointmentAPITests(TestCase):
    """Test the /api/appointments endpoint."""

    def setUp(self):
        self.client = Client()
        self.valid_data = {
            'name': 'Test User',
            'age': '30',
            'sex': 'Male',
            'contact': '+91 98765 43210',
        }

    def test_get_not_allowed(self):
        """GET requests should be rejected (POST only)."""
        response = self.client.get('/api/appointments')
        self.assertEqual(response.status_code, 405)

    def test_valid_submission_returns_200(self):
        """A valid appointment submission should return 200."""
        response = self.client.post(
            '/api/appointments',
            data=json.dumps(self.valid_data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('message', data)
        self.assertIn('Booking confirmed', data['message'])

    def test_valid_submission_with_int_age(self):
        """Age sent as integer should not crash the server."""
        payload = self.valid_data.copy()
        payload['age'] = 30  # integer, not string
        response = self.client.post(
            '/api/appointments',
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)

    def test_missing_name_returns_400(self):
        """Missing name should return 400."""
        payload = self.valid_data.copy()
        payload['name'] = ''
        response = self.client.post(
            '/api/appointments',
            data=json.dumps(payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_missing_all_fields_returns_400(self):
        """Empty payload should return 400."""
        response = self.client.post(
            '/api/appointments',
            data=json.dumps({}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_json_returns_400(self):
        """Malformed JSON should return 400."""
        response = self.client.post(
            '/api/appointments',
            data='this is not json',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())


class NotificationMethodTests(TestCase):
    """Test that the notification routing logic works correctly."""

    def setUp(self):
        self.client = Client()
        self.valid_data = {
            'name': 'Notification Test',
            'age': '25',
            'sex': 'Female',
            'contact': '9999999999',
        }
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(self.base_dir, 'data', 'config.json')
        # Save original config
        with open(self.config_path, 'r') as f:
            self.original_config = f.read()

    def tearDown(self):
        # Restore original config
        with open(self.config_path, 'w') as f:
            f.write(self.original_config)

    def _set_config(self, method):
        with open(self.config_path, 'w') as f:
            json.dump({'notification_method': method}, f)

    @patch('appointments.views.send_mail')
    def test_email_only_calls_send_mail(self, mock_send_mail):
        """When set to 'email', send_mail should be called."""
        self._set_config('email')
        with self.settings(EMAIL_HOST_USER='test@test.com', RECEIVER_EMAIL='admin@test.com'):
            response = self.client.post(
                '/api/appointments',
                data=json.dumps(self.valid_data),
                content_type='application/json',
            )
        self.assertEqual(response.status_code, 200)
        mock_send_mail.assert_called_once()

    @patch('appointments.views.requests.post')
    def test_whatsapp_only_calls_api(self, mock_post):
        """When set to 'whatsapp', requests.post to Meta API should be called."""
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        self._set_config('whatsapp')
        with self.settings(
            WHATSAPP_PHONE_NUMBER_ID='12345',
            WHATSAPP_ACCESS_TOKEN='token123',
            ADMIN_WHATSAPP_NUMBER='9876543210',
        ):
            response = self.client.post(
                '/api/appointments',
                data=json.dumps(self.valid_data),
                content_type='application/json',
            )
        self.assertEqual(response.status_code, 200)
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertIn('graph.facebook.com', call_args[0][0])

    @patch('appointments.views.requests.post')
    @patch('appointments.views.send_mail')
    def test_both_calls_email_and_whatsapp(self, mock_send_mail, mock_post):
        """When set to 'both', both send_mail and requests.post should be called."""
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        self._set_config('both')
        with self.settings(
            EMAIL_HOST_USER='test@test.com',
            RECEIVER_EMAIL='admin@test.com',
            WHATSAPP_PHONE_NUMBER_ID='12345',
            WHATSAPP_ACCESS_TOKEN='token123',
            ADMIN_WHATSAPP_NUMBER='9876543210',
        ):
            response = self.client.post(
                '/api/appointments',
                data=json.dumps(self.valid_data),
                content_type='application/json',
            )
        self.assertEqual(response.status_code, 200)
        mock_send_mail.assert_called_once()
        mock_post.assert_called_once()

    @patch('appointments.views.send_mail')
    def test_whatsapp_only_does_not_call_email(self, mock_send_mail):
        """When set to 'whatsapp', send_mail should NOT be called."""
        self._set_config('whatsapp')
        response = self.client.post(
            '/api/appointments',
            data=json.dumps(self.valid_data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        mock_send_mail.assert_not_called()

    @patch('appointments.views.requests.post')
    def test_email_only_does_not_call_whatsapp(self, mock_post):
        """When set to 'email', requests.post should NOT be called."""
        self._set_config('email')
        response = self.client.post(
            '/api/appointments',
            data=json.dumps(self.valid_data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        mock_post.assert_not_called()


class StaticFileTests(TestCase):
    """Test that static file references exist in the HTML."""

    def setUp(self):
        self.client = Client()

    def test_css_referenced(self):
        """The page should link to styles.css."""
        response = self.client.get('/')
        self.assertContains(response, 'css/styles.css')

    def test_js_referenced(self):
        """The page should link to script.js."""
        response = self.client.get('/')
        self.assertContains(response, 'js/script.js')

    def test_font_awesome_referenced(self):
        """The page should link to Font Awesome."""
        response = self.client.get('/')
        self.assertContains(response, 'font-awesome')

    def test_google_fonts_referenced(self):
        """The page should link to Google Fonts."""
        response = self.client.get('/')
        self.assertContains(response, 'fonts.googleapis.com')
