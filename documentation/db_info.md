<img src="https://raw.githubusercontent.com/tjouni/messageboard/master/documentation/diagram.png" width=800>

### Create table statements

```
CREATE TABLE account (
	id INTEGER NOT NULL,
	date_created DATETIME,
	date_modified DATETIME,
	name VARCHAR(144) NOT NULL,
	username VARCHAR(144) NOT NULL,
	password VARCHAR(144) NOT NULL,
	email VARCHAR(144) NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (username)
);
CREATE TABLE role (
	id INTEGER NOT NULL,
	role VARCHAR(20) NOT NULL,
	PRIMARY KEY (id)
);
CREATE TABLE category (
	id INTEGER NOT NULL,
	name VARCHAR(50) NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (name)
);
CREATE TABLE user_role (
	account_id INTEGER,
	role_id INTEGER,
	FOREIGN KEY(account_id) REFERENCES account (id),
	FOREIGN KEY(role_id) REFERENCES role (id)
);
CREATE TABLE user_category (
	account_id INTEGER,
	category_id INTEGER,
	FOREIGN KEY(account_id) REFERENCES account (id),
	FOREIGN KEY(category_id) REFERENCES category (id)
);
CREATE TABLE thread (
	id INTEGER NOT NULL,
	date_created DATETIME,
	date_modified DATETIME,
	title VARCHAR(64) NOT NULL,
	category_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(category_id) REFERENCES category (id)
);
CREATE INDEX ix_thread_category_id ON thread (category_id);
CREATE TABLE message (
	id INTEGER NOT NULL,
	date_created DATETIME,
	date_modified DATETIME,
	thread_id INTEGER NOT NULL,
	user_id INTEGER,
	message_text VARCHAR NOT NULL,
	original_post BOOLEAN NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(thread_id) REFERENCES thread (id),
	FOREIGN KEY(user_id) REFERENCES account (id) ON DELETE SET NULL,
	CHECK (original_post IN (0, 1))
);
CREATE INDEX ix_message_thread_id ON message (thread_id);
```
