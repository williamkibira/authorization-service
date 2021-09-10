CREATE TABLE session_tb (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_identifier VARCHAR NOT NULL,
	user_id INT NOT NULL,
	initiated_at  TIMESTAMP NOT NULL,
	expires_at  TIMESTAMP NOT NULL,
	status VARCHAR NO NULL DEFAULT 'ACTIVE',
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	idx INT,
	CONSTRAINT user_fkey FOREIGN KEY (user_id) REFERENCES user_tb(id) ON DELETE CASCADE
);

CREATE TRIGGER IF NOT EXISTS update_session_idx AFTER INSERT ON session_tb
		BEGIN
		    UPDATE session_tb SET idx=id WHERE id=NEW.id;
		END;

