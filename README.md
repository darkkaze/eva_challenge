# endpoints

i follow the rest estandar and create the next endpoints

~~~
patients/
patients/<int:pk>/
patients/<int:patient_pk>/studies
patients/<int:patient_pk>/studies/<int:pk>/
~~~

the studies are anidated in the patients query, becouse all studies have one patient. i didn't see necesaria endpoints like `studies/`  `studies/<int:pk>/`


# django rest framework

i use the highest level of abstraction in rest-framework (generics: https://www.django-rest-framework.org/api-guide/generic-views/)
this part of the library give me a nice auto documentation

this autodocumentation page is in `api-docs/`  and i think is the better place for start the code challenge review

generics is very flexible when you learn to override its methods, and its pattern is good, since it forces to move part of the logic to serializers layer.


# models

I don't know how many types of body parts or studies there are, but it seemed like a good idea to create a catalog of them.
catalogs are autofilled in migrations  (`api.migrations.0002_populate_catalogs`)

generic treats catalogs with their ids. using an int-id instead of a name, it can be annoying for the client.
so i patch this for use the human readable name.  this patch is in the `api.serializers.StudySerializer`

# tests

move factory.py to tests folder, if factory is used just in test, then i think this is a better place

# .env.dist ?

writing environment variables to a file saved in the git repo is a security flaw. so I won't use it.

~~~
# settings.py
SECRET_KEY = os.getenv("SECRET_KEY") or 'dummy'
~~~

i think dummy is ok for develop and github actions.
is necesary to inject the real SECRET_KEY  in the devops process


# Docker

I only wrote the minimum necessary to make it work.

# about the app_names and table_names

I see apps as an organizational structure shaped like a tree, is a tree because the apps have hierarchies for prevent circular imports, although in directories they are at the same level.

~~~
users/   # user, signup, login, and other related stufs
organization/  # in this case, maybe hospitals? 
    patient/  # demographics, clinic history, etc.
        studie/  # clinic studies and thing related to this.
        # other examples
        scheduler/  # for manage the patient - doctor dating
    finance/  # for finance things.
    # etc, etc, etc

~~~

I disagree with the name "api" for an app. because it doesn't give me a structure for organizing all the possible thing that a project could have. but for practical purpose i keep it.

~~~
    class Meta:
        db_table = "patient"

    class Meta:
        db_table = "study"

~~~

django has a good naming convention:  app_name__table_name (pluralized)
An app is usually a set of related things, and the app prefix helps the tables appear grouped and neat in any database viewer. (when the db has hundred of tables, man gives thanks to God to be able to see them grouped by topic)

I see no reason to change this. But in the end it's trivial, so I decided to keep it


# about pipenv

I implement pipenv as they indicate, because it is somewhat trivial, but i am against its use.
pipenv simplify thing that in python already be simple, install a couple of libraries in node means install a nightmare of dependencies,  this does not happen in python,  populate and delete items from requirments.txt is a trivial task, and a good python proyect is libraryless (because python is Batteries Included)

i think the pattern of have the environment in the same folder of the proyect,  (or better, in the parent folder of the proyect) is more intuitive that pipenv pattern of hiding the environment directory.

from the devops side, usually the application lives alone in a docker container, (or another type of virtual machine). you don't need a virtualenv or additional managers to do a simple 'pip install -r requirments.txt'

https://grassfedcode.medium.com/five-myths-about-pipenv-698c5f198e4b
https://hynek.me/articles/python-app-deps-2018/