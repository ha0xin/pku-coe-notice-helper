# pku-coe-notice-helper
A small project for learning `requests` and `BeautifulSoup`. Pushes PKU offical notifications, DeanPKU announcements and COE notices to WeChat via WxPusher.

## Prerequisites
- Python 3.x
- WxPusher account

## How to Use

### 1. Clone the project to your server:
```bash
git clone https://github.com/yourusername/pku-coe-notice-helper.git
cd pku-coe-notice-helper
```

### 2. Obtain WxPusher Credentials
Follow the WxPusher [documentation](https://wxpusher.zjiecode.com/docs/) to obtain your `APPTOKEN` and `UID`. Create a `.env` file in the project root directory and fill in the following details:

```env
APPTOKEN=AT_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# To push notifications to multiple UIDs, separate them with commas
UIDS=UID_xxxxxxxxxxxxxxxxxxxxxxxxxxxx,UID_yyyyyyyyyyyyyyyyyyyyyyyyyyyy
```

### 3. Create a Virtual Environment
Use `venv` to create a virtual environment:
```bash
python -m venv venv
```

Activate the virtual environment:
- On Windows:
  ```bash
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies
Install the required Python libraries using `pip`:

```bash
pip install -r requirements.txt
```

### 5. Schedule the Script
For example, on Linux, set up a cron job:

```bash
crontab -e
```

Add the following line to run the script every hour:

```bash
0 * * * * /path/to/venv/bin/python /path/to/pku-coe-notice-helper/push.py
```

On Windows, you can use Task Scheduler to achieve a similar result.

## Contributing
Contributions of any kind are welcome! If you have any suggestions or improvements, feel free to submit a pull request or create an issue.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
