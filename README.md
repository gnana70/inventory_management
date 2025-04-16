# Inventory Management System

A comprehensive inventory management system designed to track orders from placement to completion, with support for component management, invoice tracking, and quality control.

## Features

- Order management with component tracking
- Invoice creation and management
- Quality control workflow
- Dashboard with reporting and analytics
- User, team, and role management
- Modern responsive UI

## Technology Stack

- Django 4.2 (Python web framework)
- SQLite (Development database)
- PostgreSQL (Optional production database)
- Tailwind CSS (UI framework)
- Alpine.js (JavaScript framework for reactivity)
- HTMX (Enhanced interactivity)
- Chart.js (Data visualization)

## Setup and Installation

### Prerequisites

- Python 3.11 or higher
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/Inventory.git
cd Inventory
```

### Step 2: Create and Activate Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements/development.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env
```

Open `.env` in a text editor and configure settings as needed. For development, the default SQLite configuration should work fine.

### Step 5: Apply Database Migrations

```bash
python manage.py migrate
```

### Step 6: Create Admin User

```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin account.

### Step 7: Start the Development Server

```bash
python manage.py runserver
```

The application will be available at: http://127.0.0.1:8000/

## Project Structure

- `apps/` - Django applications
  - `accounts/` - User, team, and role management
  - `orders/` - Order and component management
  - `invoices/` - Invoice management
  - `quality_control/` - QC processes
  - `dashboard/` - Reporting and analytics
- `config/` - Project configuration
- `static/` - Static files
- `templates/` - HTML templates
- `media/` - User uploads
- `requirements/` - Dependency files

## Usage

- **Admin Interface**: Access at http://127.0.0.1:8000/admin/ with your superuser credentials
- **Main Application**: Access at http://127.0.0.1:8000/ after logging in

## Development Workflow

### Running Tests

```bash
pytest
```

### Updating Dependencies

If you need to add new dependencies:

1. Add them to the appropriate requirements file:
   - `requirements/base.txt` - Core dependencies
   - `requirements/development.txt` - Development-only dependencies
   - `requirements/production.txt` - Production-only dependencies

2. Reinstall dependencies:
   ```bash
   pip install -r requirements/development.txt
   ```

## Production Deployment

For production deployment:

1. Set `DJANGO_SETTINGS_MODULE=config.settings.production` in your environment
2. Configure a PostgreSQL database
3. Set `DEBUG=False`
4. Set a secure `SECRET_KEY`
5. Configure proper email settings
6. Set up a web server like Nginx with Gunicorn

## License

This project is licensed under the MIT License - see the LICENSE file for details. 