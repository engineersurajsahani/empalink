# Empalink - Donation Management System

A Django-based web application for managing donations with multi-role authentication, story management, and transparency features.

## Features

- **Multi-role Authentication**: Admin, Donor, and Volunteer roles
- **User Registration & Login**: Secure authentication with role selection
- **Story Management**: Create, approve, and manage donation stories
- **Donation System**: Secure donation flow with payment verification
- **Receipt Generation**: PDF receipt generation for donations
- **Dashboard**: Role-based dashboards for different user types
- **Transparency Dashboard**: Public view of donation metrics
- **Notifications**: Email and in-app notifications
- **Search & Filter**: Advanced search and filtering capabilities

## Tech Stack

- **Backend**: Django
- **Frontend**: Django Templates with Bootstrap
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **Media Handling**: Pillow for image processing
- **PDF Generation**: ReportLab for receipts

## Installation

1. **Clone the repository** (or create the project structure):
   ```bash
   mkdir empalink
   cd empalink
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\Activate.ps1
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install django pillow reportlab
   ```

5. **Create Django project and apps**:
   ```bash
   django-admin startproject empalink .
   python manage.py startapp accounts
   python manage.py startapp stories
   python manage.py startapp donations
   python manage.py startapp core
   ```

6. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
empalink/
├── empalink/                 # Django project settings
├── accounts/                 # User authentication and profiles
├── stories/                  # Story management
├── donations/                # Donation processing
├── core/                     # Core functionality (notifications, etc.)
├── templates/                # HTML templates
├── static/                   # CSS, JS, and static files
├── media/                    # User uploaded media files
├── manage.py
└── requirements.txt
```

## Usage

1. **Access the application** at `http://127.0.0.1:8000/`

2. **Admin Panel**: Access at `http://127.0.0.1:8000/admin/`

3. **User Registration**: New users can register at `/accounts/signup/`

4. **Role-based Access**:
   - **Admin**: Full access to manage stories, donations, and users
   - **Donor**: Can make donations and view their donation history
   - **Volunteer**: Can create stories and showcase their contributions

## Key Functionality

### For Volunteers
- Create donation stories with title, description, category, required amount
- Upload images and supporting documents
- Track their created stories and achievements

### For Donors
- Browse approved stories
- Make donations with payment screenshot upload
- Download receipts for confirmed donations
- View donation history

### For Admins
- Approve/reject stories
- Verify donation payments
- Monitor all activities
- Generate reports

## Security Features

- Password hashing with Django's built-in authentication
- Role-based permissions
- Input validation and sanitization
- Secure file upload handling

## Customization

The application can be extended with:

- Email notifications
- Payment gateway integration (instead of manual verification)
- Advanced reporting features
- Mobile-responsive design enhancements

## Database Models

- **User**: Custom user model with role-based access
- **VolunteerProfile**: Extended profile for volunteers
- **Category**: Story categories (Medical, Education, etc.)
- **Story**: Donation stories with approval workflow
- **Donation**: Donation records with verification status
- **Receipt**: Donation receipts (PDF/HTML)
- **Notification**: System notifications

## Running the Application

1. Ensure your virtual environment is activated
2. Run migrations if not already done: `python manage.py migrate`
3. Start the development server: `python manage.py runserver`
4. Access the application at `http://127.0.0.1:8000/`

## Admin Access

- Create a superuser with: `python manage.py createsuperuser`
- Access admin panel at: `http://127.0.0.1:8000/admin/`
- Default admin credentials (after creating superuser):
  - Username: As created during superuser creation
  - Password: As set during superuser creation

## Sample Data

The application includes sample data for demonstration purposes:
- Categories: Medical, Education, Food, Emergency, Community
- Users: Admin, donors, and volunteers
- Stories: Various causes with different categories
- Donations: Sample donation records with different statuses

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is created for educational purposes.