# Get followers/following list in Instagram
This is an example in Python 3.x that show how to get followers/following list in Instagram without to use Instagram API (an scraper).

## Getting Started
Please, follow the instructions below for installing and run it.

### Pre-requisites
Make sure you have installed:
* Python 3.x
* pip3 (used to install 'requests' library)

### Installing
```bash
$ git clone https://github.com/francozanardi/get_instagram_followers-following_list giffl
$ cd giffl
$ pip3 install -r requirements.txt
```

## Usage
```bash
$ python3 get_lists.py -u username -s mySessionID
```
Where _username_ is the target and _mySessionID_ is the cookie "sessionId" of an open Instagram account.