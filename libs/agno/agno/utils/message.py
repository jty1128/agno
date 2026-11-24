from __future__ import annotations

from collections.abc import Mapping, Sequence

from agno.models.message import Message


def get_text_from_message(message: Sequence[Mapping] | Mapping | str | Message) -> str:
    """Return the user texts from the message"""

    if isinstance(message, str):
        return message
    if isinstance(message, list):
        text_messages = []
        if len(message) == 0:
            return ""

        if "type" in message[0]:
            for m in message:
                m_type = m.get("type")
                m_value = m.get(m_type)
                if (
                    m_type is not None
                    and isinstance(m_type, str)
                    and m_value is not None
                    and isinstance(m_value, str)
                    and m_type == "text"
                ):
                    text_messages.append(m_value)
                    # if m_type == "image_url":
                    #     text_messages.append(f"Image: {m_value}")
                    # else:
                    #     text_messages.append(f"{m_type}: {m_value}")
        elif "role" in message[0]:
            for m in message:
                m_role = m.get("role")
                m_content = m.get("content")
                if (
                    m_role is not None
                    and isinstance(m_role, str)
                    and m_content is not None
                    and isinstance(m_content, str)
                    and m_role == "user"
                ):
                    text_messages.append(m_content)
        if len(text_messages) > 0:
            return "\n".join(text_messages)
    if isinstance(message, dict):
        if "content" in message:
            return get_text_from_message(message["content"])
    if isinstance(message, Message) and message.content is not None:
        return get_text_from_message(message.content)
    return ""
