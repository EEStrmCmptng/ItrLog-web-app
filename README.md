# ItrLog-web-app

#### a web ui for visualizing flink query results and cpu log data, built with dash and plotly.js

<img width="919" alt="itrlog-example" src="https://user-images.githubusercontent.com/93945205/184464660-7f081f34-d256-40b2-a5bd-6e13778c93e6.png">

## Quick Start

Create python virtual environment by `python3 -m venv env`

Activiate virtual environment by `source env/bin/activate`

Install necessary modules by `pip3 install -r requirements.txt`

Start the web application by `python3 dashboard/index.py`

## Access 

Visit `localhost:8888` from your web browser. 

If you are trying to access this from bootstrap, you can use ssh tunneling by 
`ssh -L 8888:127.0.0.1:8888 bootstrap` in your terminal and then access the same link above.

