CREATE TABLE IF NOT EXISTS stars (
    message_id numeric NOT NULL,
    user_id numeric NOT NULL,
    PRIMARY KEY (message_id, user_id),

    FOREIGN KEY (message_id) REFERENCES messages (id)
        ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE CASCADE
);