# ldap-face

## config
add .env file as copy of .env.example file

secret key generation:
```
python -c 'import secrets; print(secrets.token_hex())'
```

Development backend start:
```
flask --app run --debug run
```
