# Use cases

### Unregistered user

  * Register a new account
    ```
    INSERT INTO Account
    VALUES (date_created, date_modified, name, username, password, email)
    ```


### Registered ser

  * Modify or delete your own account
    * Deleting an account doesn't delete messages or threads, instead 'DELETED USER' is shown in the username field
    ```
    DELETE FROM account WHERE account.id = ?
    ```
  * TODO: List all threads which you have a permission (category) for
  * View messages in a thread
    * Messages are shown with username and basic message information
    * Modify or delete your own messages
      * Deleting the first message in a thread deletes the whole thread
    * Edited messages have an 'EDITED'-tag
    ```
    SELECT Message.id, Message.date_created, Message.date_modified, message_text, user_id, username FROM Message
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
  
