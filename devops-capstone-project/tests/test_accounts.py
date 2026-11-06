import os
import tempfile
import unittest

from service import create_app


class AccountsApiTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        database = os.path.join(self.temp_dir.name, "test.db")
        self.app = create_app({
            "TESTING": True,
            "DATABASE_PATH": database,
            "PORT": 8080,
            "CORS_ORIGINS": ["http://localhost:3000"],
            "TALISMAN_FORCE_HTTPS": False,
        })
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_account(self, email="test@example.com"):
        return self.client.post("/accounts", json={
            "name": "Test Account",
            "email": email,
            "address": "Pune",
            "phone_number": "9876543210",
        })

    def test_create_account(self):
        response = self.create_account()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["email"], "test@example.com")

    def test_create_requires_name_and_email(self):
        response = self.client.post("/accounts", json={"name": "No email"})
        self.assertEqual(response.status_code, 400)

    def test_list_accounts(self):
        self.create_account()
        response = self.client.get("/accounts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_read_account(self):
        created = self.create_account()
        account_id = created.get_json()["id"]
        response = self.client.get(f"/accounts/{account_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], account_id)

    def test_read_missing_account(self):
        self.assertEqual(self.client.get("/accounts/999").status_code, 404)

    def test_update_account(self):
        account_id = self.create_account().get_json()["id"]
        response = self.client.put(f"/accounts/{account_id}", json={"name": "Updated"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["name"], "Updated")

    def test_update_missing_account(self):
        self.assertEqual(self.client.put("/accounts/999", json={"name": "X"}).status_code, 404)

    def test_delete_account(self):
        account_id = self.create_account().get_json()["id"]
        response = self.client.delete(f"/accounts/{account_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get(f"/accounts/{account_id}").status_code, 404)

    def test_duplicate_email(self):
        self.create_account()
        response = self.create_account()
        self.assertEqual(response.status_code, 409)

    def test_cors_allowed_origin(self):
        response = self.client.get("/accounts", headers={"Origin": "http://localhost:3000"})
        self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "http://localhost:3000")

    def test_cors_preflight(self):
        response = self.client.options(
            "/accounts",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
            },
        )
        self.assertIn(response.status_code, (200, 204))
        self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "http://localhost:3000")

    def test_security_headers(self):
        response = self.client.get("/health")
        self.assertIn("X-Content-Type-Options", response.headers)
        self.assertIn("X-Frame-Options", response.headers)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "success")


if __name__ == "__main__":
    unittest.main()
