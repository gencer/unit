import unittest
import unit

class TestUnitConfiguration(unit.TestUnitControl):

    def setUpClass():
        unit.TestUnit().check_modules('python')

    def test_json_leading_zero(self):
        self.assertIn('error', self.put('/', '00'), 'leading zero')

    def test_json_unicode(self):
        self.assertIn('success', self.put('/applications', b"""
            {
                "ap\u0070": {
                    "type": "\u0070ython",
                    "workers": 1,
                    "path": "\u002Fapp",
                    "module": "wsgi"
                }
            }
            """), 'unicode')

    def test_json_unicode_2(self):
        self.assertIn('success', self.put('/applications', """
            {
                "приложение": {
                    "type": "python",
                    "workers": 1,
                    "path": "/app",
                    "module": "wsgi"
                }
            }
            """), 'unicode 2')

    def test_json_unicode_number(self):
        self.assertIn('error', self.put('/applications', b"""
            {
                "app": {
                    "type": "python",
                    "workers": \u0031,
                    "path": "/app",
                    "module": "wsgi"
                }
            }
            """), 'unicode number')

    def test_applications_open_brace(self):
        self.assertIn('error', self.put('/applications', '{'), 'open brace')

    def test_applications_string(self):
        self.assertIn('error', self.put('/applications', '"{}"'), 'string')

    @unittest.expectedFailure
    def test_negative_workers(self):
        self.assertIn('error', self.put('/applications', """
            {
                "app": {
                    "type": "python",
                    "workers": -1,
                    "path": "/app",
                    "module": "wsgi"
                }
            }
            """), 'negative workers')

    @unittest.expectedFailure
    def test_applications_type_only(self):
        self.assertIn('error', self.put('/applications', """
            {
                "app": {
                    "type": "python"
                }
            }
            """), 'type only')

    def test_applications_miss_quote(self):
        self.assertIn('error', self.put('/applications', """
            {
                app": {
                    "type": "python",
                    "workers": 1,
                    "path": "/app",
                    "module": "wsgi"
                }
            }
            """), 'miss quote')

    def test_applications_miss_colon(self):
        self.assertIn('error', self.put('/applications', """
            {
                "app" {
                    "type": "python",
                    "workers": 1,
                    "path": "/app",
                    "module": "wsgi"
                }
            }
            """), 'miss colon')

    def test_applications_miss_comma(self):
        self.assertIn('error', self.put('/applications', """
            {
                "app": {
                    "type": "python"
                    "workers": 1,
                    "path": "/app",
                    "module": "wsgi"
                }
            }
            """), 'miss comma')

    def test_applications_skip_spaces(self):
        self.assertIn('success', self.put('/applications', b'{ \n\r\t}'),
            'skip spaces')

    def test_applications_relative_path(self):
        self.assertIn('success', self.put('/applications', """
            {
                "app": {
                    "type": "python",
                    "workers": 1,
                    "path": "../app",
                    "module": "wsgi"
                }
            }
            """), 'relative path')

    @unittest.expectedFailure
    def test_listeners_empty(self):
        self.assertIn('error', self.put('/listeners', '{"*:7080":{}}'),
            'listener empty')

    def test_listeners_no_app(self):
        self.assertIn('error', self.put('/listeners',
            '{"*:7080":{"application":"app"}}'), 'listeners no app')

    def test_listeners_wildcard(self):
        self.assertIn('success', self.put('/', """
            {
                "listeners": {
                    "*:7080": {
                        "application":"app"
                    }
                },
                "applications": {
                    "app": {
                        "type": "python",
                        "workers": 1,
                        "path": "/app",
                        "module": "wsgi"
                    }
                }
            }
            """), 'listeners wildcard')

    def test_listeners_explicit(self):
        self.assertIn('success', self.put('/', """
            {
                "listeners": {
                    "127.0.0.1:7081": {
                        "application":"app"
                    }
                },
                "applications": {
                    "app": {
                        "type": "python",
                        "workers": 1,
                        "path": "/app",
                        "module": "wsgi"
                    }
                }
            }
            """), 'explicit')

    def test_listeners_explicit_ipv6(self):
        self.assertIn('success', self.put('/', """
            {
                "listeners": {
                    "[::1]:7082": {
                        "application":"app"
                    }
                },
                "applications": {
                    "app": {
                        "type": "python",
                        "workers": 1,
                        "path": "/app",
                        "module": "wsgi"
                    }
                }
            }
            """), 'explicit ipv6')

    def test_listeners_no_port(self):
        self.assertIn('success', self.put('/', """
            {
                "listeners": {
                    "[::1]:7082": {
                        "application":"app"
                    }
                },
                "applications": {
                    "app": {
                        "type": "python",
                        "workers": 1,
                        "path": "/app",
                        "module": "wsgi"
                    }
                }
            }
            """), 'no port')

if __name__ == '__main__':
    unittest.main()
