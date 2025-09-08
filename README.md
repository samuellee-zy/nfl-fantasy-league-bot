# NFL Fantasy League

This repository contains the code for an NFL Fantasy League application.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- User authentication and authorization
- Create and manage fantasy leagues
- Draft players
- Set weekly lineups
- Track scores and standings
- Real-time updates

## Installation

To get started with the NFL Fantasy League application, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/nfl_fantasy_league.git
   cd nfl_fantasy_league
   ```

2. **Install dependencies:**

   ```bash
   # For the backend (Python/Django)
   pip install -r requirements.txt

   # For the frontend (JavaScript/React)
   cd frontend
   npm install
   ```

3. **Set up environment variables:**

   Create a `.env` file in the root of the backend directory and add the following:

   ```
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   ```

   For the frontend, create a `.env` file in the `frontend` directory:

   ```
   REACT_APP_API_URL=http://localhost:8000/api/
   ```

4. **Run database migrations (backend):**

   ```bash
   python manage.py migrate
   ```

## Usage

### Running the Backend

From the root of the repository:

```bash
python manage.py runserver
```

The backend API will be available at `http://localhost:8000/`.

### Running the Frontend

From the `frontend` directory:

```bash
npm start
# nfl-fantasy-league-bot
