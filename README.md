Data-Tag
====

Data-Tag is an evolved system to classify textual data and web pages using NLP techniques, rather than not so intelligent Keyword-based Tagging. It uses [NLTK](http://www.nltk.org/) to categorize data tokens into various "Word-Classes" and then using Open Data from [Wikipedia](http://www.mediawiki.org/wiki/API:Main_page) applies [Word-Sense Disambiguation](http://en.wikipedia.org/wiki/Word-sense_disambiguation) algorithm to "smartly" tag the input data.


## Setup

After Forking the Repo into your account...

Use `git clone` to clone this repo to your local machine:
```
    $ git clone https://github.com/rishy/data-tag.git
```

Install all the dependencies using `npm install`:
```
    $ npm install
```

Install all the `bower` packages:
```
    $ bower install
```

for first time, install a virtual environment in root directory using `install.sh` (or `install.bat` for Windows):
```python 
    $ chmod +x install.sh
    $ ./install.sh
```
Keep your Cool, this will take a while to install all the dependencies. ;)

##Commands

Note:- First install `Fabric` to run below commands
```shell
    $ sudo pip install fabric
```

To run an app :
```
    $ fab runapp
```

App Running on [http://127.0.0.1:5000/]([http://127.0.0.1:5000/])

## Contribution Guidelines

After Cloning the Repo...

Set the `upstream` to this repo:

The easiest way is to use the https url:
```
git remote add upstream https://github.com/rishy/data-tag.git
```

or if you have ssh set up you can use that url instead:
```
git remote add upstream git@github.com:rishy/data-tag.git
```

Working branch for **data-tag** will always be the `develop` branch. Hence, all the latest code will always be on the *develop* branch.
You should always create a new branch for any new piece of work branching from *develop* branch:
```
git branch new_branch
```
**NOTE:** You must not mess with `master` branch or bad things will happen.
*master* branch contains the latest stable code, so just leave it be.

Before starting any new piece of work, move to *develop* branch:
```
git checkout develop
```

Now you can fetch latest changes from main repo using:
```
git fetch upstream
```

`merge` the latest code with *develop* branch:
```
git merge upstream/develop
```

`checkout` to your newly created branch:
```
git checkout new_branch
```

Rebase the code of *new_branch* from the code in *develop* branch, run the `rebase` command from your current branch:
```
git rebase develop
```
Now all your changes on your current branch will be based on the top of the changes in *develop* branch.

Push your changes to your forked repo
```
git push origin new_branch
```

Now, you can simply send the Pull Request to Parent Repo from within the Github.

Always squash up your commits into a single commit before sending the Pull Request. Use `git rebase -i` for this purpose. For example to squash last 3 commits into a single commit, simply run:
```
git rebase -i HEAD~3
```

For any changes in `requirements.txt`, you will have to run
```
flask/bin/pip install -r requirements.txt
```
