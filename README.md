# README Backend

# .env and config.json
The .env file is used to store values that need to be changed, such as credentials.
In the config.json, values are stored that don't have to be changed and are not security relevant. Such as: list of supported languages, categories of boats, categories of users etc.


# Supported languages
Supported languages are *de-CH* and *fr-CH*. They are defined in *backend/models/config.py*


# Roles
The following roles exist: Admin, Manager and User
The role "User" allow access to basic function. With the Role "Manager", a user can create and manage instance-wide events.

With the role Admin, the user can edit other users (accepted / verified).

Important: All roles that apply must be added to the user (e.g. a Admin that wants to use the app needs to have all the roles Admin, Manager and User).