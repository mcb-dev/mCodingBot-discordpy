USERS = """CREATE TABLE IF NOT EXISTS users (
    id numeric PRIMARY KEY
);"""

MESSAGES = """CREATE TABLE IF NOT EXISTS messages (
    id numeric PRIMARY KEY,
    channel_id numeric NOT NULL,
    author_id numeric NOT NULL,

    points int NOT NULL DEFAULT 0,

    starboard_message_id numeric DEFAULT NULL,
    -- starboard_channel_id is set in config

    FOREIGN KEY (author_id) REFERENCES users (id)
        ON DELETE SET NULL
);"""

STARS = """CREATE TABLE IF NOT EXISTS stars (
    message_id numeric NOT NULL,
    user_id numeric NOT NULL,
    PRIMARY KEY (message_id, user_id),

    FOREIGN KEY (message_id) REFERENCES messages (id)
        ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE CASCADE
);"""

ALL_TABLES = [USERS, MESSAGES, STARS]
