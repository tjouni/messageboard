# Use cases

### Unregistered user

  * Register a new account
    ```
    INSERT INTO Account
    VALUES (date_created, date_modified, name, username, password, email)
    ```


### Registered user

  * Modify or delete your own account
    * Deleting an account doesn't delete messages or threads, instead 'DELETED USER' is shown in the username field
    ```
    DELETE FROM account WHERE account.id = ?
    ```
  * List all threads which you have a permission (category) for
    ```
    SELECT thread.id AS thread_id, thread.date_created AS thread_date_created,
           thread.date_modified AS thread_date_modified, thread.title AS thread_title,
           thread.category_id AS thread_category_id FROM thread
    ```
  * View messages in a thread
    * Messages are shown with username and basic message information
    * Modify or delete your own messages
      * Deleting the first message in a thread deletes the whole thread
    * Edited messages have an 'EDITED'-tag displayed in message title row
    ```
    SELECT Message.id, Message.date_created, Message.date_modified, message_text, user_id, username
    FROM Message
    LEFT JOIN Account ON Message.user_id = Account.id
    WHERE thread_id = ?
    ORDER BY Message.id ASC
    ```
  * Create new threads
    ```
    INSERT INTO Thread
    VALUES (date_created, date_modified, title, category_id)

    INSERT INTO Message
    VALUES (date_created, date_modified, thread_id, user_id, message_text, original_post)
    ```
  * Reply to existing threads
    * Replying to a message updates the date modified field for the thread
  

### Administrator

  * All basic user functionalities
  * Remove and modify any user account
  * Remove and modify any message
  * Add and remove roles and categories
    ```
    INSERT INTO role (role) VALUES (?);
    INSERT INTO category (name) VALUES (?);
    ```
  * Modify all roles and categories except admin role and default category
    ```
    UPDATE role SET role=? WHERE role.id = ?
    UPDATE category SET name=? WHERE category.id = ?
    ```
  * Modify categories and roles for all users
    ```
    INSERT INTO user_role (account_id, role_id) VALUES (?, ?);
    DELETE FROM user_role (account_id, role_id) WHERE account_id = ? AND role_id = ?;
    INSERT INTO category_role (account_id, category_id) VALUES (?,?);
    DELETE FROM user_category (account_id, category_id) WHERE account_id = ? AND category_id = ?;
    ```
  * View roles and number of users in each role
    ```
    SELECT Role.id, Role.role, (SELECT COUNT(DISTINCT a.id) FROM Role as r2
    JOIN user_role AS ur ON Role.id = ur.role_id
    JOIN account AS a ON ur.account_id = a.id) AS usercount FROM Role
    GROUP BY Role.id;
    ```
  * View categories and number of threads and users in each category
    ```
    SELECT Category.id, Category.name, COUNT(Thread.id) as threadcount,
     (SELECT COUNT(a.id) FROM Category AS c
      JOIN user_category AS uc ON c.id = uc.category_id AND c.id = Category.id
      JOIN account AS a ON uc.account_id = a.id) AS usercount FROM Category
    LEFT JOIN Thread ON Thread.category_id = Category.id
    GROUP BY Category.id;
    
