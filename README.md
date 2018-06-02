# story_post

* API documnetation:
	* signup_author API:
		This api will help the author to signup for the first time to use the service. This will store the login information in the system.
		
		sample curl: curl -X POST \
  http://localhost:9000/signup_author \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 190a70fa-757e-ced6-4ea4-a1f998f2d4d3' \
  -d '{"mobile": "your mobile number", "password": "password", "name": "Bichitra"}'
	
	* add_new_stories API:
		this POST api will enable the author to add stories as drafts and as well as post. This can be called from draft button and post button.
		
		a sample curl for this api: curl -X POST \
  http://localhost:9000/add_new_stories \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: ed91f482-6fa5-ae8c-4722-09c1d513c712' \
  -H 'mobile: 'your signup number'' \
  -H 'password: 'enter your password here'' \
  -d '{"title": "My first post", "draft": "cdsjhbfv", "tags": "me,you"}'
	
	* edit_story API:
		This POST api help you edit existing story. This need the story id  and author id to edit the story. It can post a draft as story change story datas.
		This api will be triggered by a button which will be located against each story which will be visible in the web.
		
		a sample curl: curl -X POST \
  http://localhost:9000/edit_story \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 98fd67dc-da0d-8e28-33af-e33a9ce06cf5' \
  -H 'mobile: 'mobile' \
  -H 'password: your password' \
  -d '{"id": 2, "tags": ["check"]}'
	
	* get_stories API: This will give all the publiced stories and all the drafts of author. This have the ability of search by author name, tags, title etc.
	This have capability of sorting the record by creation date, updatation date and author name both ascending and descending order.
	
		a sample curl: curl -X GET \
  http://localhost:9000/get_stories \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: cb11f48a-f364-5e92-5743-0a38ede2768b' \
  -H 'mobile: your mobile number' \
  -H 'password: your password'
	
* Assumption:
	* For now getting user number and password for each time calling a API. but it will chage to resource_id
	* this app does not have requirements.txt file. so expecting to have environment which have all the dependencies.
	
* Setup the APP:
	*	Before setting up delete all the revision files in migrations/revisions
	* change the db url in apis/__init__.py
	* run python migrate.py db migrate to generate migration file 
	* run python migrate.py db upgrade to set up table in your db
	* signup into the system using signup API to be able to use the system
