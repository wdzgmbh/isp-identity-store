

# isp-identity-store

isp-identity-store claims to be a one-stop-shop for authenticating customers.

## Current Features

+ Accounts
  + LineID (according to https://ak-spri.de/wp-content/uploads/Struktur-und-Semantik-der-LineID_V.1.4.pdf)
  + Bandwidth
+ IPoE Authentication
  + Authenticate via LineID

## Components

### isp_identity_store

isp_identity_store is a Django project to provide API endpoints for multiple use-cases.
The FreeRADIUS REST module needs to use API endpoints for authenticating users.
The ISP needs to use API endpoints to create, read, update and delete Accounts to the datastore.

The RADIUS endpoint is currently tested with RtBrick.

### deployment

deployment contains a standard FreeRADIUS setup, which is configured to use the API from isp_identity_store.
Do not use this FreeRADIUS setup in production.

Start the FreeRADIUS deployment with `docker-compose up --build`.

### test_client

test_client is a test client for testing the RADIUS authentication, because radtest is not good enough for our use cases.

## Configuration

TBD


