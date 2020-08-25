# Coffee Shop Full Stack Project

Udacity has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard. But they need help setting up their menu experience.

The goal of this project is to create a full stack drink menu application. The application:

1. Displays graphics representing the ratios of ingredients in each drink.
2. Allows public users to view drink names and graphics.
3. Allows the shop baristas to see the recipe information.
4. Allows the shop managers to create new drinks and edit existing drinks.

## About the Stack

This full stack application has been designed with some key functional areas:

### Backend

The `./backend` directory contains a completed Flask server with a pre-written SQLAlchemy module to simplify your data needs. You will need to configure and integrate Auth0 for authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. You will only need to update the environment variables found within (./frontend/src/environment/environment.ts) to reflect the Auth0 configuration details set up for the backend app.

[View the README.md within ./frontend for more details.](./frontend/README.md)
