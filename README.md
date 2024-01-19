# formaloo-backend

## Description
Building an Appstore system for users, so they can create, sell, and buy application
- we have 3 entities (`User`, `Application`, `PurchasedApplication`)
- Each user can, sell and buy more than application
- Each application can be owned by only one user

## Database Schema
![alt text](https://github.com/a-samir97/formaloo-backend/blob/main/docs/database.png)

## How to run the projects ?
- All you need to run `docker-compose up`

## API endpoints 
- Auth Endpoints
  - `/api/auth/register` for signup a new user to the system
  - `/api/auth/login` for login existing user to our system
  - `/api/auth/refresh/` for refreshing access token for existing user
- Application Endpoints
  - `/apps/`: `GET Method` to get application that created by the authenticated user (requested user)
  - `/apps/`: `POST Method` to create a new application
  - `/apps/<app_id>/`: `GET Method` to retireve an application using application ID
  - `/apps/<app_id>/`: `PUT OR PATCH Method` to update an existing application using application ID
  - `/apps/<app_id>/`: `DELETE Method` to delete an existing application using application ID
- Purchased Application Endpoints
  - `/api/purchased/apps/`: `GET Method` to get all purchased apps for the authenticated user (requested user)
  - `/api/purchased/apps/<purchased_app_id>/`: `GET Method` to retrieve a purchased application using purchased application id
- Unpurchased Application Endpoint
  - `/api/unpurchased/apps/`: `GET Method` to get all unpurchased apps (and not created by requested user)
- Purchase Endpoint
  - `/api/purchase/`: `POST Method` to buy an existing application
  - Request Body : {"app_id": <app_id>}
     
## Swagger Page 
![alt text](https://github.com/a-samir97/formaloo-backend/blob/main/docs/swagger.png)
## Notes and Improvments

## Tools and Frameworks
- Python
- Django
- Django Rest Framework
- PostgreSQL Database
- Swagger
- Docker
- Docker Compose

## Dashboard Service
create a new app called `dashboard` app in our django project, then we can use `appstore` models in our dashboard app
- for example, we need to get all created application ( then we need to split this into `verified app` and not `verified app`)
- `Application.objects.count()` all created apps
- `Application.objects.filter(is_verified=True).count()` all created and verified apps
- `Application.objects.filter(is_verified=False).count()` all created and not verified apps
and we can serve this data in an endpoint called `dashboard/apps/` for example
