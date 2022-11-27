![Test](https://github.com/rowmateproject/rowmate-v2-backend/actions/workflows/test.yml/badge.svg)

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

# About user flags
We only want to grant access to users that have been accepted by the organisation / admin.
To simplify security checks, this should be handled on the login functions and not on the routers individually.
There already is a check in fastapi-users that is implemented in the login: we can activate that only users with verified E-Mail-Addresses can login (is_verified).
To achieve our goal, we use "is_verified" to describe whether users have been accepted (is_accepted) by the organisation *and* have verified their E-Mail-Address (is_email_verified).
We can achieve this by simply patching the verify()-function in the user manager.

The following flags will then exist:
- is_superuser : For superusers
- is_verified : Boolean: is_accepted AND is_email_verified
- is_email_verified: If E-Mail-Address has been verified
- is_active : Some random flag from fastapi-users? Generally set to true. Don't rely on it for security checks.

Flag 