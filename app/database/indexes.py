MESSAGES_STARBOARD_MESSAGE = (
    """CREATE UNIQUE INDEX IF NOT EXISTS
    messages_starboard_message
    ON messages (starboard_message_id)"""
)

ALL_INDEXES = [
    MESSAGES_STARBOARD_MESSAGE
]
