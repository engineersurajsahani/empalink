import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'empalink.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create superuser
username = 'admin'
email = 'admin@empalink.com'
password = 'admin123'

# Check if user already exists
if User.objects.filter(username=username).exists():
    print(f"User {username} already exists!")
else:
    user = User.objects.create_superuser(username, email, password)
    user.role = 'admin'  # Set the role to admin for superuser
    user.save()
    print(f"Superuser {username} created successfully!")