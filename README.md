# Asciipy

<img src="https://github.com/sereaf/asciipy/blob/master/images/asciipy_logo.jpg" alt="Asciipy Logo" width="500" height="500">

_Convert images and videos to ascii art and you can print them to the terminal or save them in image / video formats or in .txt file._

---

<!--## Install

```bash
pip install asciipy
```-->

<!-- [see here on pypi.org]() -->

## Requirements

-   opencv-python
-   pillow

## Usage
#### Code

```python
from asciipy import AsciiVideo, AsciiImage

# image
img_path = 'C:\image_to_ascii\your_image.png'
image = AsciiImage(img_path)
image.ascii_img() # save, return or display an ascii image
image.ascii_terminal() # print an ascii image to the terminal
image.ascii_txt() # put it into a txt file

#video
video_path = 'C:\video_to_ascii\your_video.mp4'
video = AsciiVideo(video_path)
video.ascii_video() # save or return an ascii video
video.ascii_terminal() #print an ascii video to the terminal
video.ascii_txt() # put it into a txt file

# input image can already be loaded
# by opencv or pillow, just pass that as an argument

# see all arguments bellow
```

#### Cli

```bash
asciipy -f C:\image_to_ascii\your_image.png
```

## Arguments

**Type `-h` or `--help` into the cli to get all descriptions**

| Cli                        | Desc.                                                           | Options                                  |
| -------------------------- | --------------------------------------------------------------- | ---------------------------------------- |
| -f / --file                | Input file path (or already loaded image)                       | `str`                                    |
| -ac / --action             | Return, save, show, play                                        | `'return'`, `'save'`, `'show'`, `'play'` |
| -o / --output              | Out put file path                                               | `'terminal'`, `'save'`, `'text'`         |
| -oa / --output-as          | Output to - terminal, save, text  (only cli)                    | `str`                                    |
| -op / --option             | Option to use when converting                                   | `str`                                    |
| -ch / --chars              | Characterset                                                    | `str`                                    |
| -au / --audio              | With audio                                                      | `bool`                                   |
| -fo / --font               | Font file                                                       | `str`                                    |
| -as / --save-as            | Save with give extension                                        | `str`                                    |
| -s / --scale               | Scale compared to deafult img/video size                        | `float`                                  |
| -df / --density-flip       | Reverse the given charachterset (dark, light chars flip)        | `bool`                                   |
| -cs / --character-space    | Character spacing on the image                                  | `'sm'`, `'bg'`, `'avg'`                  |
| -fs / --font-scale         | Font scale compared to the default scale of the font file       | `float`                                  |
| -ts / --terminal-size      | Terminal size - width, height ex. 50, 30                        | `int` (width, height)                    |
| -rt / --ratio-to           | Terminal printing ratio. Keep image ratio to width or to height | `'width'`, `'height'`, `'pass'`          |
| -tspc / --terminal-spacing | Character to divide the ascii characters in the terminal        | `str`                                    |
| -tclr / --terminal-clear   | Clear terminal after printing image there                       | `bool`                                   |

**In code you can pass these as keyword arguments, with always the same name as the longer version of the cli flag**

## Examples

```bash
asciipy -f test.png -oa terminal -df True -op bandw
```

```python
img = AsciiImage('test.jpg')
img.ascii_txt(density_flip=False)
```

```python
img = AsciiVideo('test.mp4')
img.ascii_video(output_as='save', charcter_space='avg',
font='C:\Windows\Fonts\Segoepr.ttf', font_scale=0.5)
```
<!--![Output Image1](https://github.com/sereaf/asciipy/blob/master/images/asciipy_terminal_bandw.png)-->
|  <img src="https://github.com/sereaf/asciipy/blob/master/images/asciipy_terminal_bandw.png" alt="First Output" width="480" height="270"> | <img src="https://github.com/sereaf/asciipy/blob/master/images/asciipy_terminal_bandw.png" alt="Second Output" width="480" height="270"> |
| ------------------ | ------------------ |

![Output Video]()

#### More...

![Output Images]()

## Support
######...
