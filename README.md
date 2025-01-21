# Shared-car-system

Shared-car-system is an electric vehicle (EV) sharing management system built with Django and the Google Maps API. It provides convenient EV rental services for users and efficient vehicle management, rental tracking, repair logging, and payment processing features for administrators. The system also includes a monthly subscription feature for users who prefer renting on a monthly basis.

---

## Features

1. **Vehicle Management**:
   - Displays EVs on a map, allowing users to select and save locations of vehicles.
   - Automatically decreases battery charge by 1% every 5 minutes when renting.
   - Manages vehicle status, including repair needs, parking status, and location.

2. **Rental Management**:
   - Users can rent available vehicles, with rental records automatically generated.
   - Tracks rental start time, end time, and return location.

3. **Repair Management**:
   - Logs repair history, including malfunction type, report date, description, operator, fix status, and repair date.

4. **Payment & Subscription**:
   - Users can make payments.
   - A monthly subscription option allows users to rent vehicles on a monthly basis.

5. **User Management**:
   - Manages user information and accounts, including registration, login, balance, contact information, and card details.

---

## Tech Stack

- **Backend**: Django
- **Frontend**: Django Templates, JavaScript, Google Maps API, Bootstrap
- **Database**: SQLite (or other compatible databases)
- **Other**: Google Maps API for map interactions

---

## Project Architecture

The project uses an MVC architecture with the following key components:

- **Models**: Define the main data structures of the system, including users, vehicles, locations, rental records, repair logs, and payment records.
- **Views**: Provide APIs and pages to operate and display data.
- **Templates**: Django frontend templates to render the user interface.

---

## Data Model Design

### User
- Fields: Username, password, surname, firstname, telephone, email, registration date, user type, account status, profile image, balance, card type, and card expiry date.

### Vehicle
- Fields: evId, vehicle type, latitude/longitude, remaining charge, repair need, parked status, last location.

### Location
- Fields: location name, address, latitude/longitude, availability status.

### RentLog
- Fields: customer (User), vehicle, start date, end date, and return location.

### RepairLog
- Fields: malfunction type, report date, customer (User), vehicle, description, operator, fixed status, and repair date.

### Payment
- Fields: customer (User), remark, amount, and payment date.

---

## Environment Setup

1. **Clone the Project**:
   ```bash
   git clone  https://stgit.dcs.gla.ac.uk/programming-and-systems-development-m/2024/lb02-09/lab-2-team-9-team-project.git
   cd EVShare
   ```

2. **Install Dependencies**:
   Ensure Python 3.x is installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Google Maps API**:
   - Obtain a Google Maps API key and add it to the project’s configuration.

4. **Database Migration**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser** (for admin management):
   ```bash
   python manage.py create_roles operator
   python manage.py create_roles manager
   ```

6. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

---

## Usage Example

- Access `http://127.0.0.1:8000/` to open the frontend interface.
- Log in or register, and view the map to select an EV.
- Admins can manage vehicle status, user accounts, repair logs, and more from the admin interface.

---

## Maintenance and Development

- **Code Style**: We recommend following PEP8 standards.
- **Testing**: Basic unit tests are included. Run `python manage.py test` to ensure functionality.
- **Contributions**: Contributions are welcome through issues and pull requests.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Future Plans

- Add more payment options and a reward points system.
- Provide detailed vehicle status monitoring and analytics reports.
- Enhance user experience, including multi-language and multi-device support.

---

Thank you for using EVShare! I hope this system makes EV sharing easier and more efficient. Feel free to reach out with any questions or suggestions!
```
