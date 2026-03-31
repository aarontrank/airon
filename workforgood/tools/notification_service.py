"""
Tool: notification_service
Sends email, SMS, or push notifications to volunteers and staff.
Replace the stub methods with real delivery integrations for your environment.
"""

from typing import Any


def send_message(
    recipient_id: str,
    channel: str,               # "email" | "sms" | "push"
    subject: str,
    body: str,
) -> dict[str, Any]:
    """
    Send a single message to a recipient via the specified channel.

    Returns:
        {
            "delivered": bool,
            "message_id": str,
            "error": str | None,
        }
    """
    raise NotImplementedError("Replace with real notification delivery")


def send_bulk(
    messages: list[dict],       # each: {"recipient_id", "channel", "subject", "body"}
) -> dict[str, Any]:
    """
    Send messages to multiple recipients.

    Returns:
        {
            "sent": [...],          # recipient_ids successfully delivered
            "failed": [...],        # recipient_ids that failed
            "delivery_rate": float,
        }
    """
    raise NotImplementedError("Replace with real bulk notification delivery")
