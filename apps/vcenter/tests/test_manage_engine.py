from unittest.mock import patch

from django.test import TestCase

from common.modules.manage_engine import ManageEngine


class ManageEngineTestCase(TestCase):
    @patch("requests.post")
    def test_add_note_to_ticket(self, mock_post):
        manage_engine = ManageEngine()
        ticket_id = 123
        message = "Test message"
        comment_input_data = {
            "note": {
                "description": message,
                "show_to_requester": True,
                "mark_first_response": False,
                "add_to_linked_requests": True,
            }
        }
        manage_engine.add_note_to_ticket(ticket_id, message)

        mock_post.assert_called_once_with(
            f"{manage_engine.ticket_base_api}/{ticket_id}/notes",
            headers=manage_engine.headers,
            data={"input_data": str(comment_input_data)},
            verify=False,
        )

    @patch("requests.put")
    def test_change_ticket_status(self, mock_put):
        manage_engine = ManageEngine()
        ticket_id = 123
        status = "In Progress"
        status_input_data = {"request": {"status": {"id": status}}}
        manage_engine.change_ticket_status(ticket_id, status)

        mock_put.assert_called_once_with(
            f"{manage_engine.ticket_base_api}/{ticket_id}",
            headers=manage_engine.headers,
            data={"input_data": str(status_input_data)},
            verify=False,
        )
