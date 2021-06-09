CREATE TABLE IF NOT EXISTS messages (
    id numeric PRIMARY KEY,
    channel_id numeric NOT NULL,
    author_id numeric NOT NULL,

    points int NOT NULL DEFAULT 0,

    starboard_message_id numeric DEFAULT NULL,
    -- starboard_channel_id is set in config

    FOREIGN KEY (author_id) REFERENCES users (id)
        ON DELETE SET NULL
);