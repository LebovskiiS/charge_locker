# Charger Locker

This application is designed to organize the process of booking charging stations in building communities. It includes features like displaying spots from the database, booking, session management, and automatic session termination.

---

## Table of Contents
1. [Description](#description)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Requirements](#requirements)
5. [Features](#features)
6. [Contribution](#contribution)
7. [License](#license)

---

## Description

The project addresses the issue of disorganized shared use of charging stations in apartment complexes and other communities.

### How It Works
- Before occupying a spot, the user scans a **QR code**, which redirects them to the application page.
- Here, they can view all **available spots** for booking and select a spot.
- The user specifies the time they plan to vacate the spot and books it.
- Sessions are **automatically managed** (end or extend), and session-related data is deleted when the time expires or the user ends it manually.

### Key Features:
- Shows the **top three spots** that will be available the soonest to avoid conflicts.
- Manages user sessions with encrypted tokens stored in cookies.
- Follows the **MVC architecture** and avoids using ORMs or pre-built tools such as Flask sessions for a fully manual implementation.

This project was created to address personal needs with a focus on hands-on coding.

---

## Installation

To get started, clone the repository and install dependencies:

```bash
# Clone the repository
git clone git@github.com:LebovskiiS/charge_locker.git

# Navigate to the project directory
cd charger_locker

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

Since the application uses SQLite and Flask, it is lightweight and requires no additional setup. Everything should work out of the box.

### Example of Running the Application:
Run the application from the `main.py` file located in the project's root directory:

```python
if __name__ == '__main__':
    logger.warning('The app started')
    app.run(debug=True, port=4000, host='0.0.0.0')
```

You can change the port to any other four-digit number if the default port (`4000`) is busy.

---

## Requirements

Below are the dependencies required for the project:

- `blinker==1.9.0`
- `click==8.1.7`
- `Flask==3.1.0`
- `itsdangerous==2.2.0`
- `Jinja2==3.1.4`
- `MarkupSafe==3.0.2`
- `psycopg2-binary==2.9.10`
- `PyJWT==2.9.0`
- `python-dotenv==1.0.1`
- `SQLAlchemy==2.0.36`
- `typing_extensions==4.12.2`
- `Werkzeug==3.1.3`

Install them using the command: 

```bash
pip install -r requirements.txt
```

---

## Features

The main features of the application are as follows:

- **QR Code Integration**: Users can scan QR codes to access the booking functionality.
- **Realtime Availability**: Displays all available charging spots.
- **Automatic Session Handling**: Sessions are deleted after the expiration time or when the user manually stops the session.
- **User Tokens**: Encrypted metadata about the user is stored in cookies for session tracking.
- **Spot Forecasting**: Shows the top three nearest spots that will become available soon.
- **Lightweight and Expandable**: Built with Flask and SQLite, ensuring simple deployment.

---

## Contribution

If you have ideas or suggestions to improve the project, here's how you can contribute:

1. Fork the repository.
2. Create a branch for your feature:
   ```bash
   git checkout -b feature/NewFeature
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m 'Add a new feature'
   ```
4. Push your changes:
   ```bash
   git push origin feature/NewFeature
   ```
5. Create a Pull Request for review.

---

## License

This project is distributed under a free license. It can be copied, modified, and used, including for commercial purposes.