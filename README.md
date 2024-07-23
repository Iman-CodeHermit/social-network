# Social Network

یک شبکه اجتماعی ساده که با استفاده از Django توسعه داده شده است.

## ویژگی‌ها

- ثبت‌نام و ورود کاربران
- پروفایل کاربران
- ارسال و نمایش پست‌ها
- لایک و کامنت‌گذاری
- دنبال کردن کاربران

## پیش‌نیازها

- Python 3.11
- Django 5.0.7

## نصب

برای نصب و اجرای پروژه، مراحل زیر را دنبال کنید:

1. کلون کردن مخزن:
   
    git clone https://github.com/username/social-network.git
    cd social-network
    
2. ایجاد و فعال‌سازی محیط مجازی:
   
    python -m venv venv
    source venv/bin/activate  # در ویندوز: venv\Scripts\activate
    
3. نصب وابستگی‌ها:
   
    pip install django
    
4. اجرای مهاجرت‌های پایگاه داده:
   
    python manage.py migrate
    
5. ایجاد ابرکاربر (superuser):
   
    python manage.py createsuperuser
    
6. اجرای سرور توسعه:
   
    python manage.py runserver
    
## استفاده

برای استفاده از پروژه، پس از اجرای سرور توسعه به آدرس زیر بروید:
