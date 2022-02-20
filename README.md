If you have an enterprise airtable account and struggle with how to identify who has access to what, this project is for you.

First grab this base: https://airtable.com/shrvrts2Ehkv9Ad4m and make a copy of it. Download the code in the repo and setup the venv as shown below.

Then simply run the command: 
```bash
python3 Runner.py -a [airtable api key] -b [base id] -w [workspace id]
```
It'll take a minute or so, but you'll then be able to visually inspect the bases, the workspace collaborators and base collaaborators as well as their permissions within the airtable bases we all know and love.


Working on the Repo:

one time:
```bash
python3.7 -m venv venv/
source venv/bin/activate
cd app
pip install -r requirements.txt
```

each time:
```bash
source venv/bin/activate
```


