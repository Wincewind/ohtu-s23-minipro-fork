# Miniproject

![GHA_workflow_badge](https://github.com/turunenv/ohtu-s23-miniprojekti/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/turunenv/ohtu-s23-miniprojekti/graph/badge.svg?token=ZYGSDB5DQM)](https://codecov.io/gh/turunenv/ohtu-s23-miniprojekti)


## Backlogs
- [Backlogs](https://github.com/users/turunenv/projects/1)
- [Task estimation and burndown chart](https://docs.google.com/spreadsheets/d/1_CVzRfBNQlAJu8JO0la84PiaUmfVOdazKIZoOWZOVVI/edit#gid=0)

## Definition of Done

- Requirements met.
- Python test coverage at a decent level
- Pushed to main branch and main branch is not broken.

## Installation

1. Install poetry:
```
poetry install
```

2. Enter virtual environment with the command:
```
poetry shell
```

3. Run initialization procedures with the command:
```
python3 src/build.py
```

4. Start the app with the command:
```
python3 src/index.py
```

## Manual

### Running the app

You can run the app in the virtual environment.

Enter virtual environment with the command:
```
poetry shell
```

Start the app with the command:
```
python3 src/index.py
```

### Commands

The app will open to the starting menu:
```
Type "help" to list commands and their descriptions
Command (add or list or delete)
```

If you type ***help*** the app prints the following:
```
To EXIT the program simply press enter in the starting menu
add:      Add a new reference by provinding the required information
list:     List all stored references
delete:   Delete a reference using its reference key
cancel:   Return to the starting menu
```

#### Listing references

If you type ***list*** the app will print a table of added references.

#### Adding a reference

If you type ***add*** you can add a new reference.
```
Type "cancel" to cancel
Give source type:
```
Currently the only supported source type is book.
If you type ***cancel*** before a reference is added, you can cancel adding a reference and return to the starting menu.
The required information for a book are:

- Reference key
- Author
- Title
- Year
- Publisher

Once a reference is successfully added, the app will print:
```
ADDED!
```

#### Deleting a reference

If you type ***delete*** you can delete an existing reference.
```
Type "cancel" to cancel
Give source reference key:
```
To delete a reference you need the correct reference key. You can check by using the command ***list*** to see all sources and their reference keys.

After giving the key the app asks for confimation. To confirm write capital or lowercase y.
```
y
```
Any other value will cancel the deletion

#### Closing the app

You can close the app by pressing enter in the starting menu:
```
Type "help" to list commands and their descriptions
Command (add or list or delete)
```
