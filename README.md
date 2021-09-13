# Task manager
[![Actions Status](https://github.com/Evglit/python-project-lvl4/workflows/hexlet-check/badge.svg)](https://github.com/Evglit/python-project-lvl4/actions)
[![Python CI](https://github.com/Evglit/python-project-lvl4/actions/workflows/pyci.yml/badge.svg)](https://github.com/Evglit/python-project-lvl4/actions/workflows/pyci.yml)<br>
<a href="https://codeclimate.com/github/Evglit/python-project-lvl4/maintainability"><img src="https://api.codeclimate.com/v1/badges/d612ea874e9d73728643/maintainability" /></a>
<a href="https://codeclimate.com/github/Evglit/python-project-lvl4/test_coverage"><img src="https://api.codeclimate.com/v1/badges/d612ea874e9d73728643/test_coverage" /></a><br>

## Description
The <b>task management</b> system that allows you to set tasks, assign performers and change their statuses. Registration and authentication are required to work with the system.<br>

The project is deployed to Heroku: [https://task-mg.herokuapp.com](https://task-mg.herokuapp.com)<br>

Password for all users: `123`<br>

Login example:<br>
Username: `Тирион`<br>
Password: `123`

## Installation
Clone the repository and use this command to install application dependencies:<br>
``` bash
pip install -r requirements.txt
```

The following environment variables are used to configure the application:<br>
`POST_SERVER_ITEM_ACCESS_TOKEN`
`SECRET_KEY_APP`
`DEBUG_STATUS`
`ALLOWED_HOSTS`