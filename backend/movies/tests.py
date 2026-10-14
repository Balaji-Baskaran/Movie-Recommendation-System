import json
from django.test import TestCase, Client
from django.urls import reverse


class MovieAPITests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_health(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "healthy")
        self.assertGreater(data.get("movies_loaded", 0), 0)

    def test_movies_list(self):
        response = self.client.get('/api/movies')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn("idx", data[0])
        self.assertIn("label", data[0])

    def test_filter_options(self):
        response = self.client.get('/api/filter-options')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("genres", data)
        self.assertIn("years", data)
        self.assertIn("industries", data)
        self.assertGreater(len(data["genres"]), 0)

    def test_search(self):
        response = self.client.post(
            '/api/search',
            data=json.dumps({"movie_idx": 0, "n": 5}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("selected", data)
        self.assertIn("recommendations", data)
        self.assertIn("chart_json", data)
        self.assertEqual(len(data["recommendations"]), 5)

    def test_filter(self):
        response = self.client.post(
            '/api/filter',
            data=json.dumps({"genres": ["Action"]}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("movies", data)
        self.assertGreater(len(data["movies"]), 0)
