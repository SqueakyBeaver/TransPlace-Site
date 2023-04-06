# TransPlace Website

## So what is this?

This is a website I made for a discord community because why not.
It is made with Django, DRF (Django Rest Framework), Bootstrap for the frontend, and probably some other things
______

## Running myself

I mean if you want to run it yourself, go ahead. It'll just be tailored to this specific Discord community.

First, you need to create a `.env` file in the root directory. This will hold your environment variables. And example is found in `.env.example`. It will tell you how to get the values you need.
After that, create a virtual environment with `python -m venv .venv` if you want and install the packages needed with `pip install --r requirements.txt`
Once that is all done, run `python manage.py makemigrations core`, `python manage.py makemigrations posts`, and `python manage.py migrate` for good measure
Run `python manage.py createsuperuser` to create a super user so you have access to `/admin/`
Run `python manage.py runserver` once you're ready to run the server

____

## Url paths

| URL Path |        Explanation          |
| ----- | -----                 |
| `/about/`| This is the main index page |
| `/resources/` | This is a page like the main index page but with different content |
| `/posts/` | This is where you will find overview of all the posts |
| `/posts/<post_id>` | This will show the details of a post with the id `post_id` |
| `/auth/login` | Login with Discord |
| `/auth/login/redirect` | The Discord OAuth2 redirect (don't need to go here manually) |
| `/logout` | Logout of the website |
| `/api-auth/` | Nothing |
| `/api-auth/<Login\|Logout>` | Login/Logout of api? |
| `/api/` | Nothing |
| `/api/<posts\|users>` | API endpoint of posts or users. **Must be logged in to see** |
| `/admin/` | View Admin console. **Must be logged in** |

_____

## Questions? Comments? Concerns?

Open an issue or a pull request