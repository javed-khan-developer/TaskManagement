from schemas.chat_schema import ChatRequest


def test_chat_request_can_be_instantiated():
    chat = ChatRequest(title="Test chat")
    assert chat.title == "Test chat"
