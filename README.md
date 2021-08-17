[![Discord](https://img.shields.io/discord/876769819821756466?color=%236a7ec5&label=discord&logo=discord&style=plastic)](https://discord.gg/qbDUUx3nPW)

# Splitgate live match score

Python with pytesseract OCR engine and custom trained splitgate font to get match score of splitgate game and send them to websocket server.

![image](https://user-images.githubusercontent.com/74879467/129587165-8869a8e6-9e15-46f7-89fa-3f45e76887c1.png)


## Installation

```bash
pip install -r requirements.txt
```
To make tesseract to work, you need to install an application that will communicate with python script.
(You can use tesseract from `jTessBoxEditor` too)
## Usage

```python
#SCREENSHOT COOLDOWN BETWEEN EACH SCREENSHOT AND OCR (SCREENSHOTING DOESN'T TAKE MUCH PERFORMANCE)
cooldown = 0.2
#port where local websocket will be hosted
port = 5521
```
Set your websocket port and then connect to websocket using "ws://localhost:{port}". You can use [webosocket tester](https://www.piesocket.com/websocket-tester) to test if it is working.

Otherwise, you can use the script without websocket:

```python
# without_websocket()
#if you want to disable websockets comment theese three lines and uncommend line above
start_server = websockets.serve(websocket_server, "localhost", port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Support 
If you'd like to support me you can use my code `GECR3Y` in-game :)

## License
[MIT](https://choosealicense.com/licenses/mit/)
