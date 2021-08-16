# How to create `.traindata` from font

* You may have found in multiple articles website http://trainyourtesseract.com/ but unfortunately this site doesn't exist anymore. There may be complex tutorials that you don't understand but I am here to show you simple way to create one.

* Install latest release of [jTessBoxEditor](https://github.com/nguyenq/jTessBoxEditor/releases/).

* Open the application using `train.bat`.

* Navigate `into TIFF /Box Generator` tab.

* Paste in text you want to train (For example if you want to get data from digital clock you will only put in numbers from `0` to `9` and `:`). You can use `Input` button too for large texts. Always remember if you make your training set more specific like `blue`, `red` and `gray` you will have a lot better chances detecting those words.

* Select `Output` path using the three dots `...` otherwise you will get an error .

  (The program will create bunch of files so I recommend creating new directory.)

* Select which font you want to train, after that you can click on generate.

* If generating was successful head to the `Trainer` tab.

* First select Tesseract executable. **!!! It needs to be executable from the program path !!!** (`/jTessBoxEditor/tesseract-ocr` and select random file and press `Open` button).

* In the`Trading Data` select `.tif` file.

* In language enter `eng` (or whatever language are u using) and tick `RTL`.

* In the `-- Training Mode --` section select `Train with Existing Box` afterwards press `Run`.

* You should see your `.traindata` in `/output_directory/tessdata`.

* 

  ## How to use `.traindata` file

* Paste you `.traindata` file inside your `Tesseract-OCR/tessdata` (Installation folder) by default installation folder is `%LOCALAPPDATA%\Programs\Tesseract-OCR` so you should copy it to `%LOCALAPPDATA%\Programs\Tesseract-OCR\tessdata`

* In python you can use `lang` attribute when doing `OCR`, for example:

  ```python
  FONT_NAME = "Arial" #Your font here, for example Arial (Arial is trained by default so training it would be useless)
  
  imageText = pytesseract.image_to_string(image, lang=FONT_NAME, config=config)
  ```

