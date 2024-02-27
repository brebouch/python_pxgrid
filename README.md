# Simple pxGrid Python App

## Requirements

1. System with Python3 installed
2. A reachable ISE deployment
3. ISE pxGrid template client certificate

## Installation

1. Clone Repository ```git clone {{REPO}}```
2. CD into cloned directory ``cd {{REPO}}``
3. Install Python dependencies ```pip install -r requirements.txt```
4. Add pxGrid certificates to *certs/* directory 

## Usage

Main.py provides usage for the query session by IP and the query all sessions functions. It can be run by entering the following:

```bash
python3 main.py 10.1.1.1
```

The IP address following is optional, when main.py executes it performs a check to see if an IP address was provided. If so,
it will do a lookup for session by the IP before providing a summary on all sessions. If the IP is omitted, it will just
provide the session summary.

