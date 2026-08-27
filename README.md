# TNEA Counselling Portal (Demo / Learning Project)

A Django clone of the general shape of the TNEA (Tamil Nadu Engineering
Admissions) counselling website: registration, login, a cutoff-based
college search, college listings, and a student dashboard for saving
options. Built for learning purposes — it is **not** affiliated with or a
replacement for the official government TNEA portal, and the sample
cutoff data is randomly generated, not real.

## Features

- Student registration & login (Django's built-in auth)
- Community-wise cutoff search (enter your mark + community, optionally
  filter by branch, get a ranked list of eligible college/branch options)
- College listing and detail pages showing all cutoffs per college
- Student dashboard to save/track chosen options
- Django admin for managing colleges, branches, and cutoff records

## Setup

1. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Load sample data** (colleges, branches, cutoffs)
   ```bash
   python manage.py seed_data
   ```

5. **Create an admin user** (optional, to use /admin/)
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. Open **http://127.0.0.1:8000/** in your browser.
   - `/register/` — create a student account
   - `/cutoff-search/` — search eligible colleges by mark & community
   - `/colleges/` — browse all colleges
   - `/dashboard/` — view saved options (after login)
   - `/admin/` — manage data (after creating a superuser)

## Project structure

```
tnea_portal/
├── manage.py
├── requirements.txt
├── tnea_portal/          # project settings, urls, wsgi
└── counseling/            # the main app
    ├── models.py           # College, Branch, Cutoff, StudentProfile, Application
    ├── views.py
    ├── forms.py
    ├── admin.py
    ├── management/commands/seed_data.py   # sample data generator
    ├── templates/
    └── static/counseling/css/style.css
```

## Extending it

Ideas if you want to take this further:
- Replace the random `seed_data` command with real historical cutoff data
  (as CSV import) if you have a legitimate dataset to work from.
- Add preference ordering / ranking to `Application` for a real
  "choice filling" workflow.
- Add rank-based (not just mark-based) eligibility logic.
- Paginate the college list and cutoff search results.
- Style pass with a CSS framework if you want a closer visual match.
-
