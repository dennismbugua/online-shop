# Building-an-Online-Shop

Your online shop will enable clients to browse products, add them to the cart, apply discount codes, go through the checkout process, pay with a credit card, and obtain an invoice. You will also implement a recommendation engine to recommend products to your customers, and you will use internationalization to offer your site in multiple languages.

**Functionalities include:**

- Create a product catalog
- Build a shopping cart using Django sessions
- Create custom context processors
- Manage customer orders
- Configure Celery in your project with RabbitMQ as a message broker
- Send asynchronous notifications to customers using Celery
- Monitor Celery using Flower

- Integrate the Stripe payment gateway into your project
- Process credit card payments with Stripe
- Handle payment notifications
- Export orders to CSV files
- Create custom views for the administration site
- Generate PDF invoices dynamically

- Creating a coupon system
- Applying coupons to the shopping cart
- Applying coupons to orders
- Creating coupons for Stripe Checkout
- Storing products that are usually bought together
- Building a product recommendation engine with Redis



Build a basic online shop. Create a catalog of products and implement a shopping cart using Django sessions. Create custom context processors and launch asynchronous tasks using Celery.

Integrate a payment gateway into your site to let users pay by credit card. Extend the administration site to export orders to CSV format and generate PDF invoices

Add a coupon system to your shop. Learn how internationalization and localization work, and build a recommendation engine

---

**Building a shopping cart**

Create a shopping cart so that users can pick the products that they want to purchase. A shopping cart allows users to select products and set the amounts they want to order, and then store this information temporarily, while they browse the site until they eventually place an order. The cart has to be persisted in the session so that the cart items are maintained during the user's visit.

We will use Django's session framework to persist the cart. The cart will be kept in the session until it finishes or the user checks out of the cart.

---

**Using Django sessions**

Django provides a session framework that supports anonymous and user sessions. The session framework allows you to store arbitrary data for each visitor. Session data is stored on the server side, and cookies contain the session ID unless you use the cookie-based session engine. The session middleware manages the sending and receiving of cookies. The default session engine stores session data in the database, but you can choose between different session engines.

To use sessions, you have to make sure that the MIDDLEWARE setting of your project contains 'django.contrib.sessions.middleware.SessionMiddleware'. This middleware manages sessions. It's added by default to the MIDDLEWARE setting when you create a new project using the startproject command.

The session middleware makes the current session available in the request object. You can access the current session using request.session, treating it like a Python dictionary to store and retrieve session data. The session dictionary accepts any Python object by default that can be serialized to JSON. 

**You can set a variable in the session like this:**

request.session['foo'] = 'bar'

**Retrieve a session key as follows:**

request.session.get('foo')

**Delete a key you previously stored in the session as follows:**

del request.session['foo']

You can just treat request.session like a standard Python dictionary.

When users log in to the site, their anonymous session is lost and a new session is created for the authenticated users. If you store items in an anonymous session that you need to keep after the user logs in, you will have to copy the old session data into the new session.

---

**Session settings**

There are several settings you can use to configure sessions for your project. The most important is SESSION_ENGINE. This setting allows you to set the place where sessions are stored. By default, Django stores sessions in the database using the Session model of the django.contrib.sessions application.

Django offers the following options for storing session data:

- Database sessions: Session data is stored in the database. This is the default session engine.
- File-based sessions: Session data is stored in the filesystem.
- Cached sessions: Session data is stored in a cache backend. You can specify cache backends using the CACHES setting. Storing session data in a cache system provides the best performance.
- Cached database sessions: Session data is stored in a write-through cache and database. Reads-only use the database if the data is not already in the cache.
- Cookie-based sessions: Session data is stored in the cookies that are sent to the browser.

For better performance, use a cache-based session engine. Django supports Memcached out of the box and you can find third-party cache backends for Redis and other cache systems.

You can customize sessions with specific settings. Here are some of the important session-related settings:

- SESSION_COOKIE_AGE: The duration of session cookies in seconds. The default value is 1209600 (two weeks).
- SESSION_COOKIE_DOMAIN: The domain used for session cookies. Set this to mydomain.com to enable cross-domain cookies or use None for a standard domain cookie.
- SESSION_COOKIE_SECURE: A boolean indicating that the cookie should only be sent if the connection is an HTTPS connection.
- SESSION_EXPIRE_AT_BROWSER_CLOSE: A boolean indicating that the session has to expire when the browser is closed.
- SESSION_SAVE_EVERY_REQUEST: A boolean that, if True, will save the session to the database on every request. The session expiration is also updated each time it's saved.

You can see all the session settings and their default values at https://docs.djangoproject.com/en/2.0/ref/settings/#sessions.

---

**Session expiration**

You can choose to use browser-length sessions or persistent sessions using the SESSION_EXPIRE_AT_BROWSER_CLOSE setting. This is set to False by default, forcing the session duration to the value stored in the SESSION_COOKIE_AGE setting. If you set SESSION_EXPIRE_AT_BROWSER_CLOSE to True, the session will expire when the user closes the browser, and the SESSION_COOKIE_AGE setting will not have any effect.

You can use the set_expiry() method of request.session to overwrite the duration of the current session.

---

**Storing shopping carts in sessions**

We need to create a simple structure that can be serialized to JSON for storing cart items in a session. The cart has to include the following data for each item contained in it:

- The ID of a Product instance
- Quantity selected for the product
- Unit price for the product

Since product prices may vary, we take the approach of storing the product's price along with the product itself when it's added to the cart. By doing so, we use the current price of the product when users add it to their cart, no matter if the product's price is changed afterwards.

Now, you have to build functionality to create carts and associate them with sessions. The shopping cart has to work as follows:

- When a cart is needed, we check if a custom session key is set. If no cart is set in the session, we create a new cart and save it in the cart session key.
- For successive requests, we perform the same check and get the cart items from the cart session key. We retrieve the cart items from the session and their related Product objects from the database.

---

**Creating shopping cart views**

Now that we have a Cart class to manage the cart, we need to create the views to add, update, or remove items from it. We need to create the following views:

- A view to add or update items in a cart, which can handle current and new quantities
- A view to remove items from the cart
- A view to display cart items and totals

---

**Creating a context processor for the current cart**

You might have noticed that the message Your cart is empty is displayed in the header of the site, even when the cart contains items. We should display the total number of items in the cart and the total cost instead. Since this has to be displayed in all pages, we will build a context processor to include the current cart in the request context, regardless of the view that processes the request.

---

**Context processors**

A context processor is a Python function that takes the request object as an argument and returns a dictionary that gets added to the request context. They come in handy when you need to make something available globally to all templates.

By default, when you create a new project using the startproject command, your project contains the following template context processors, in the context_processors option inside the TEMPLATES setting:

- django.template.context_processors.debug: This sets the boolean debug and sql_queries variables in the context representing the list of SQL queries executed in the request.
- django.template.context_processors.request: This sets the request variable in the context.
- django.contrib.auth.context_processors.auth: This sets the user variable in the request.
- django.contrib.messages.context_processors.messages: This sets a messages variable in the context containing all messages that have been generated using the messages framework.

Django also enables django.template.context_processors.csrf to avoid cross-site request forgery attacks. This context processor is not present in the settings, but it is always enabled and cannot be turned off for security reasons.

You can see the list of all built-in context processors at https://docs.djangoproject.com/en/2.0/ref/templates/api/#built-in-template-context-processors.

---

**Registering customer orders**

When a shopping cart is checked out, you need to save an order into the database. Orders will contain information about customers and the products they are buying.

---

**Creating customer orders**

We will use the order models we created to persist the items contained in the shopping cart when the user finally places an order. A new order will be created following these steps:

- Present users an order form to fill in their data
- Create a new Order instance with the data entered, and create an associated OrderItem instance for each item in the cart
- Clear all the cart content and redirect users to a success page

---

**Launching asynchronous tasks with Celery**

Everything you execute in a view affects response times. In many situations, you might want to return a response to the user as quickly as possible and let the server execute some process asynchronously. This is especially relevant for time-consuming processes or processes subject to failure, which might need a retry policy. For example, a video sharing platform allows users to upload videos but requires a long time to transcode uploaded videos. The site might return a response to users to inform them that the transcoding will start soon, and start transcoding the video asynchronously. Another example is sending emails to users. If your site sends email notifications from a view, the SMTP connection might fail or slow down the response. Launching asynchronous tasks is essential to avoid blocking the code execution.

Celery is a distributed task queue that can process vast amounts of messages. It does real-time processing but also supports task scheduling. Using Celery, not only can you create asynchronous tasks easily and let them be executed by workers as soon as possible, but you can also schedule them to run at a specific time.

You can find the Celery documentation at http://docs.celeryproject.org/en/latest/index.html.

**Installing Celery**

`pip install celery`

Celery requires a message broker in order to handle requests from an external source. The broker takes care of sending messages to Celery workers, which process tasks as they receive them.

**Installing RabbitMQ**

There are several options to choose as a message broker for Celery, including key/value stores such as Redis, or an actual message system such as RabbitMQ. We will configure Celery with RabbitMQ, since it's the recommended message worker for Celery.

- install RabbitMQ

After installing it, launch RabbitMQ using the following command from the shell:

`rabbitmq-server`

You will see output that ends with the following line:

Starting broker... completed with 10 plugins.

---

**Adding asynchronous tasks to your application**

We are going to create an asynchronous task to send an email notification to our users when they place an order. The convention is to include asynchronous tasks for your application in a tasks module within your application directory.

Open another shell and start the Celery worker from your project directory, using the following command:

`celery -A myshop worker -l info`

---

**Monitoring Celery**

You might want to monitor the asynchronous tasks that are executed. Flower is a web-based tool for monitoring Celery. You can install Flower using this command:

`pip install flower`

Once installed, you can launch Flower by running the following command from your project directory:

`celery -A myshop flower`

Open http://localhost:5555/dashboard in your browser. You will be able to see the active Celery workers and asynchronous task statistics

You can find documentation for Flower at https://flower.readthedocs.io/.

---

**Integrating a payment gateway**

A payment gateway allows you to process payments online. Using a payment gateway, you can manage customer's orders and delegate payment processing to a reliable, secure third party. You won't have to worry about processing credit cards in your own system.

There are several payment gateway providers to choose from. We are going to integrate Braintree, which is used by popular online services such as Uber or Airbnb. Braintree provides an API that allows you to process online payments with multiple payment methods such as a credit card, PayPal, Android Pay, and Apple Pay. You can learn more about Braintree at https://www.braintreepayments.com/.

Braintree provides different integration options. The simplest is the Drop-in integration, which contains a pre-formatted payment form. However, in order to customize the behavior and experience of our checkout, we are are going to use the advanced Hosted Fields integration. You can learn more about the Hosted Fields integration at https://developers.braintreepayments.com/guides/hosted-fields/overview/javascript/v3.

Certain payment fields on the checkout page, such as the credit card number, CVV number, or expiration date, must be hosted securely. The Hosted Fields integration hosts the checkout fields on the payment gateway's domain and renders an iframe to present the fields to the users. This provides you with the ability to customize the look and feel of the payment form, while ensuring that you are compliant with Payment Card Industry (PCI) requirements. Since you can customize the look and feel of the form fields, users won't notice the iframe.

---

**Integrating the payment gateway**

The checkout process will work as follows:

- Add items to the shopping cart
- Check out the shopping cart
- Enter credit card details and pay

---

**Integrating Braintree using Hosted Fields**

The Hosted Fields integration allows you to create your own payment form using custom styles and layout. An iframe is added dynamically to the page using the Braintree JavaScript SDK. The iframe includes the Hosted Fields payment form. When the customer submits the form, Hosted Fields collects the card details securely and attempts to tokenize them. If tokenization succeeds, you can send the generated token nonce to your view to make a transaction using the Python braintree module.

We will create a view for processing payments. The whole checkout process will work as follows:

- In the view, a client token is generated using the braintree Python module. This token is used in the next step to instantiate the Braintree JavaScript client; it's not the payment token nonce.
- The view renders the checkout template. The template loads the Braintree JavaScript SDK using the client token and generates the iframe with the hosted payment form fields.
- Users enter their credit card details and submit the form. A payment token nonce is generated with the Braintree JavaScript client. We send the token to our view with a POST request.
- The payment view receives the token nonce and we use it to generate a transaction using the braintree Python module.

---

**Testing payments**

Open a shell and run RabbitMQ with the following command:

`rabbitmq-server`

Open another shell and start the Celery worker from your project directory with the following command:

`celery -A myshop worker -l info`

Open one more shell and start the development server with this command:

- python manage.py runserver

Open http://127.0.0.1:8000/ in your browser, add some products to the shopping cart, and fill in the checkout form. When you click the PLACE ORDER button, the order will be persisted to the database, the order ID will be saved in the current session, and you will be redirected to the payment process page.

Braintree provides a list of successful and unsuccessful credit cards so that you can test all possible scenarios. You can find a list of credit cards for testing at https://developers.braintreepayments.com/guides/credit-cards/testing-go-live/python.

**Going live**

Once you have tested your environment, you can create a real Braintree account at https://www.braintreepayments.com. Once you are ready for moving into production, remember to change your live environment credentials in the settings.py file of your project and use braintree.Environment.Production to set up your environment. All steps to go live are summarized at https://developers.braintreepayments.com/start/go-live/python .

---

**Exporting orders to CSV files**

Sometimes, you might want to export the information contained in a model to a file so that you can import it in any other system. One of the most widely used formats to export/import data is Comma-Separated Values (CSV). A CSV file is a plain text file consisting of a number of records. There is usually one record per line, and some delimiter character, usually a literal comma, separates the record fields. We are going to customize the administration site to be able to export orders to CSV files.

---

**Extending the admin site with custom views**

Sometimes, you may want to customize the administration site beyond what is possible through configuring ModelAdmin, creating admin actions, and overriding admin templates. If this is the case, you need to create a custom admin view. With a custom view, you can build any functionality you need. You just have to make sure that only staff users can access your view and that you maintain the admin look and feel by making your template extend an admin template.

---

**Generating PDF invoices dynamically**

Now that we have a complete checkout and payment system, we can generate a PDF invoice for each order. There are several Python libraries to generate PDF files. One popular library to generate PDFs with Python code is Reportlab. You can find information about how to output PDF files with Reportlab at https://docs.djangoproject.com/en/2.0/howto/outputting-pdf/.

In most cases, you will have to add custom styles and formatting to your PDF files. You will find it more convenient to render an HTML template and convert it into a PDF file, keeping Python away from the presentation layer. We are going to follow this approach and use a module to generate PDF files with Django. We will use WeasyPrint, which is a Python library that can generate PDF files from HTML templates.

---

**Sending PDF files by email**

When a payment is successful, we will send an automatic email to our customers including the generated PDF invoice. Edit the views.py file of the payment application

---

**Creating a coupon system**

Many online shops give out coupons to customers that can be redeemed for discounts on their purchases. An online coupon usually consists of a code that is given to users, valid for a specific time frame. The code can be redeemed one or multiple times.

We are going to create a coupon system for our shop. Our coupons will be valid for clients that enter the coupon in a specific time frame. The coupons will not have any limitations in terms of the number of times they can be redeemed, and they will be applied to the total value of the shopping cart. For this functionality, we will need to create a model to store the coupon code, a valid time frame, and the discount to apply.

---

**Applying a coupon to the shopping cart**

We can store new coupons and make queries to retrieve existing coupons. Now we need a way for customers to apply coupons to their purchases. The functionality to apply a coupon would be as follows:

- The user adds products to the shopping cart.
- The user can enter a coupon code in a form displayed in the shopping cart detail page.
- When a user enters a coupon code and submits the form, we look for an existing coupon with the given code that is currently valid. We have to check that the coupon code matches the one entered by the user that the active attribute is True, and that the current datetime is between the valid_from and valid_to values.
- If a coupon is found, we save it in the user's session and display the cart, including the discount applied to it and the updated total amount.
- When the user places an order, we save the coupon to the given order.

---

**Adding internationalization and localization**

Django offers full internationalization and localization support. It allows you to translate your application into multiple languages and it handles locale-specific formatting for dates, times, numbers, and time zones. Let's clarify the difference between internationalization and localization. Internationalization (frequently abbreviated to i18n) is the process of adapting software for the potential use of different languages and locales, so that it isn't hardwired to a specific language or locale. Localization (abbreviated to l10n) is the process of actually translating the software and adapting it to a particular locale. Django itself is translated into more than 50 languages using its internationalization framework.

---

**Internationalization with Django**

The internationalization framework allows you to easily mark strings for translation both in Python code and in your templates. It relies on the GNU gettext toolset to generate and manage message files. A message file is a plain text file that represents a language. It contains a part, or all, of the translation strings found in your application and their respective translations for a single language. Message files have the .po extension.

Once the translation is done, message files are compiled to offer rapid access to translated strings. The compiled translation files have the .mo extension.

---

**Internationalization and localization settings**

Django provides several settings for internationalization. The following settings are the most relevant ones:

- USE_I18N: A Boolean that specifies whether Django's translation system is enabled. This is True by default.
- USE_L10N: A Boolean indicating whether localized formatting is enabled. When active, localized formats are used to represent dates and numbers. This is False by default.
- USE_TZ: A Boolean that specifies whether datetimes are time zone-aware. When you create a project with the startproject command, this is set to True.
- LANGUAGE_CODE: The default language code for the project. This is in standard language ID format, for example, 'en-us' for American English, or 'en-gb' for British English. This setting requires USE_I18N to be set to True in order to take effect. You can find a list of valid language IDs at http://www.i18nguy.com/unicode/language-identifiers.html.
- LANGUAGES: A tuple that contains available languages for the project. They come in two tuples of a language code and language name. You can see the list of available languages at django.conf.global_settings. When you choose which languages your site will be available in, you set LANGUAGES to a subset of that list.
- LOCALE_PATHS: A list of directories where Django looks for message files containing translations for this project.
- TIME_ZONE: A string that represents the time zone for the project. This is set to 'UTC' when you create a new project using the startproject command. You can set it to any other time zone, such as 'Europe/Madrid'.

These are some of the internationalization and localization settings available. You can find the full list at https://docs.djangoproject.com/en/2.0/ref/settings/#globalization-i18n-l10n.

---

**Internationalization management commands**

Django includes the following management commands to manage translations:

- makemessages: This runs over the source tree to find all strings marked for translation and creates or updates the .po message files in the locale directory. A single .po file is created for each language.
- compilemessages: This compiles the existing .po message files to .mo files that are used to retrieve translations.

You will need the gettext toolkit to be able to create, update, and compile message files. Most Linux distributions include the gettext toolkit. If you are using macOS X, probably the simplest way to install it is via Homebrew at https://brew.sh/ with the command brew install gettext. You might also need to force link it with the command brew link gettext --force. For Windows, follow the steps at https://docs.djangoproject.com/en/2.0/topics/i18n/translation/#gettext-on-windows.

---

**How to add translations to a Django project**

Let's take a look at the process to internationalize our project. We will need to do the following:

- Mark strings for translation in our Python code and our templates
- Run the makemessages command to create or update message files that include all translation strings from our code
- Translate the strings contained in the message files and compile them using the compilemessages management command

---

**How Django determines the current language**

Django comes with a middleware that determines the current language based on request data. This is the LocaleMiddleware middleware that resides in django.middleware.locale. LocaleMiddleware performs the following tasks:

- If you are using i18_patterns, that is, you use translated URL patterns, it looks for a language prefix in the requested URL to determine the current language.
- If no language prefix is found, it looks for an existing LANGUAGE_SESSION_KEY in the current user's session.
- If the language is not set in the session, it looks for an existing cookie with the current language. A custom name for this cookie can be provided in the LANGUAGE_COOKIE_NAME setting. By default, the name for this cookie is django_language.
- If no cookie is found, it looks for the Accept-Language HTTP header of the request.
- If the Accept-Language header does not specify a language, Django uses the language defined in the LANGUAGE_CODE setting.

By default, Django will use the language defined in the LANGUAGE_CODE setting unless you are using LocaleMiddleware. The process described here only applies when using this middleware.

---

**Translating Python code**

To translate literals in your Python code, you can mark strings for translation using the gettext() function included in django.utils.translation. This function translates the message and returns a string. The convention is to import this function as a shorter alias named _ (underscore character).

You can find all the documentation about translations at https://docs.djangoproject.com/en/2.0/topics/i18n/translation/.

---

**Lazy translations**

Django includes lazy versions for all of its translation functions, which have the suffix _lazy(). When using the lazy functions, strings are translated when the value is accessed, rather than when the function is called (this is why they are translated lazily). The lazy translation functions come in handy when strings marked for translation are in paths that are executed when modules are loaded.

Using gettext_lazy() instead of gettext(), strings are translated when the value is accessed rather than when the function is called. Django offers a lazy version for all translation functions.

---

**Translating templates**

Django offers the {% trans %} and {% blocktrans %} template tags to translate strings in templates. In order to use the translation template tags, you have to add {% load i18n %} at the top of your template to load them.

---

**The {% blocktrans %} template tag**

The {% blocktrans %} template tag allows you to mark content that includes literals and variable content using placeholders.

---

**Using the Rosetta translation interface**

Rosetta is a third-party application that allows you to edit translations using the same interface as the Django administration site. Rosetta makes it easy to edit .po files and it updates compiled translation files.

---

**Fuzzy translations**

You might have noticed that there is a FUZZY column in Rosetta. This is not a Rosetta feature; it is provided by gettext. If the fuzzy flag is active for a translation, it will not be included in the compiled message files. This flag marks translation strings that need to be reviewed by a translator. When .po files are updated with new translation strings, it is possible that some translation strings are automatically flagged as fuzzy. This happens when gettext finds some msgid that has been slightly modified. gettext pairs it with what it thinks was the old translation and flags it as fuzzy for review. The translator should then review fuzzy translations, remove the fuzzy flag, and compile the translation file again.

---

**URL patterns for internationalization**

Django offers internationalization capabilities for URLs. It includes two main features for internationalized URLs:

- Language prefix in URL patterns: Adding a language prefix to URLs to serve each language version under a different base URL
- Translated URL patterns: Translating URL patterns so that every URL is different for each language

A reason for translating URLs is to optimize your site for search engines. By adding a language prefix to your patterns, you will be able to index a URL for each language instead of a single URL for all of them. Furthermore, by translating URLs into each language, you will provide search engines with URLs that will rank better for each language.

---

**Adding a language prefix to URL patterns**

Django allows you to add a language prefix to your URL patterns. For example, the English version of your site can be served under a path starting /en/, and the Spanish version /es/.

To use languages in URL patterns, you have to use the LocaleMiddleware provided by Django. The framework will use it to identify the current language from the requested URL.

---

**Translating URL patterns**

Django supports translated strings in URL patterns. You can use a different translation for each language for a single URL pattern. You can mark URL patterns for translation the same way you would do with literals, using the ugettext_lazy() function.

Edit the main urls.py file of the myshop project and add translation strings to the regular expressions of the URL patterns for the cart, orders, payment, and coupons applications


Open the shell and run the next command to update the message files with the new translations:

`django-admin makemessages --all`

Make sure the development server is running. Open http://127.0.0.1:8000/en/rosetta/ in your browser and click the Myshop link under the Spanish section. Now you will see the URL patterns for translation. You can click on Untranslated only to only see the strings that have not been translated yet. You can now translate the URLs.

---

**Translating models with django-parler**

Django does not provide a solution for translating models out of the box. You have to implement your own solution to manage content stored in different languages, or use a third-party module for model translation. There are several third-party applications that allow you to translate model fields. Each of them takes a different approach to storing and accessing translations. One of these applications is django-parler. This module offers a very effective way to translate models and it integrates smoothly with Django's administration site.

django-parler generates a separate database table for each model that contains translations. This table includes all the translated fields and a foreign key for the original object that the translation belongs to. It also contains a language field, since each row stores the content for a single language.

---

**Integrating translations in the administration site**

django-parler integrates smoothly with the Django administration site. It includes a TranslatableAdmin class that overrides the ModelAdmin class provided by Django to manage model translations.

---

**Format localization**

Depending on the user's locale, you might want to display dates, times, and numbers in different formats. The localized formatting can be activated by changing the USE_L10N setting to True in the settings.py file of your project.

When USE_L10N is enabled, Django will try to use a locale-specific format whenever it outputs a value in a template. You can see that decimal numbers in the English version of your site are displayed with a dot separator for decimal places, while in the Spanish version they are displayed using a comma. This is due to the locale formats specified for the es locale by Django. You can take a look at the Spanish formatting configuration at https://github.com/django/django/blob/stable/2.0.x/django/conf/locale/es/formats.py.

Normally, you will set the USE_L10N setting to True and let Django apply the format localization for each locale. However, there might be situations in which you don't want to use localized values. This is especially relevant when outputting JavaScript or JSON that has to provide a machine-readable format.

Django offers a {% localize %} template tag that allows you to turn on/off localization for template fragments. This gives you control over localized formatting. You will have to load the l10n tags to be able to use this template tag. The following is an example of how to turn localization on and off in a template:

```
{% load l10n %}

{% localize on %}
  {{ value }}
{% endlocalize %}

{% localize off %}
  {{ value }}
{% endlocalize %}
```

Django also offers the localize and unlocalize template filters to force or avoid localization of a value. These filters can be applied as follows:

{{ value|localize }}
{{ value|unlocalize }}


You can also create custom format files to specify locale formatting. You can find further information about format localization at https://docs.djangoproject.com/en/2.0/topics/i18n/formatting/.

---

**Using django-localflavor to validate form fields**

django-localflavor is a third-party module that contains a collection of specific utils, such as form fields or model fields that are specific for each country. It's very useful to validate local regions, local phone numbers, identity card numbers, social security numbers, and so on. The package is organized into a series of modules named after ISO 3166 country codes.

---

**Building a recommendation engine**

A recommendation engine is a system that predicts the preference or rating that a user would give to an item. The system selects relevant items for the users based on their behavior and the knowledge it has about them. Nowadays, recommendation systems are used in many online services. They help users by selecting the stuff they might be interested in from the vast amount of available data that is irrelevant to them. Offering good recommendations enhances user engagement. E-commerce sites also benefit from offering relevant product recommendations by increasing their average sale.

We are going to create a simple, yet powerful, recommendation engine that suggests products that are usually bought together. We will suggest products based on historical sales, thus identifying products that are usually bought together. We are going to suggest complementary products in two different scenarios:

- Product detail page: We will display a list of products that are usually bought with the given product. This will be displayed as: Users who bought this also bought X, Y, Z. We need a data structure that allows us to store the number of times that each product has been bought together with the product being displayed.

- Cart detail page: Based on the products users add to the cart, we are going to suggest products that are usually bought together with these ones. In this case, the score we calculate to obtain related products has to be aggregated.

We are going to use Redis to store products that are purchased together.

---

**Recommending products based on previous purchases**

Now, we will recommend products to users based on what they have added to the cart. We are going to store a key in Redis for each product bought on our site. The product key will contain a Redis sorted set with scores. We will increment the score by 1 for each product bought together every time a new purchase is completed.

When an order is successfully paid for, we store a key for each product bought, including a sorted set of products that belong to the same order. The sorted set allows us to give scores for products that are bought together.

Remember to install redis-py in your environment

---

