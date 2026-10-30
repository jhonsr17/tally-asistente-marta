import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from client import AccessError, Client, validate_url

LEAD = '11111111-1111-4111-8111-111111111111'


class AccessTests(unittest.TestCase):
    def test_rejects_invalid_host_and_credentials_in_url(self):
        for url in ['http://example.com', 'https://user:password@example.com', 'https://example.com/api', 'https://example.com?token=secret']:
            with self.assertRaises(AccessError):
                validate_url(url)

    def test_blocks_id_path_escape_before_request(self):
        calls = []
        c = Client(lambda *args: calls.append(args))
        with self.assertRaises(AccessError):
            c.lead('../agencia')
        self.assertEqual(calls, [])

    def test_refuses_unconfirmed_pipeline_before_mail(self):
        calls = []
        def transport(path, params=None):
            calls.append(path)
            return {'row': {'pipeline': 'agencia'}}
        with self.assertRaises(AccessError):
            Client(transport).threads(LEAD)
        self.assertEqual(len(calls), 1)

    def test_refuses_arbitrary_mailbox_or_thread(self):
        calls = []
        def transport(path, params=None):
            calls.append(path)
            if path.endswith('/threads'):
                return {'threads': [{'thread_id': 'abc', 'mailbox': 'sales@example.com'}]}
            return {'row': {'pipeline': 'us_mx'}}
        with self.assertRaises(AccessError):
            Client(transport).thread(LEAD, 'abc', 'other@example.com')
        self.assertEqual(len(calls), 2)

    def test_allows_indexed_thread_and_preserves_partial_state(self):
        def transport(path, params=None):
            if path.endswith('/threads'):
                return {'partial': True, 'failed_mailboxes': ['missing@example.com'],
                        'threads': [{'thread_key': 'sales@example.com:abc'}]}
            if path.endswith('/abc'):
                return {'messages': [], 'mailbox': params['mailbox']}
            return {'row': {'pipeline': 'us_mx'}}
        c = Client(transport)
        self.assertTrue(c.threads(LEAD)['partial'])
        self.assertEqual(c.thread(LEAD, 'abc', 'sales@example.com')['mailbox'], 'sales@example.com')


if __name__ == '__main__':
    unittest.main()
