# YouTube Scene Recognition

YouTube 截圖場景辨識

## Table of Contents

- [Scenes](#scenes)
- [Run Application](#run-application)
  - [Prerequisites](#prerequisites)
  - [Usage](#usage)
- [Recognition Rules](#recognition-rules)
- [Labels](#labels)

## Scenes

- 主頁 (Home)
    - 留言 (Comment)
- 短影片 (Shorts)
    - 留言 (Comment)
- 影片 (Video)
    - 留言 (Comment)
    - 影片動作 (Video Action)


## Run Application

### Prerequisites

- 放入 `yolov3` model 的設定檔:

  - `metadata` (預設路徑: `./model_config/yolov3.data`)
  - `config` (預設路徑: `./model_config/yolov3.cfg`)
  - `weights` (預設路徑: `./model_config/yolov3_training2.weights`)
  
- 放入 Google OCR API 的 credentials:

  - `credentials` (預設路徑: `./processor/text_processor/credentials.json`)

### Usage

```
Usage: python3 -m processor.darknet
```

## Recognition Rules  

Do 'main scene recognition' first, and then do 'sub scene recognition' within main each scene.

- main scene recognition:

  - home:

    - existence of yolo_label 'home'
    
  - shorts:

    - existence of yolo_label 'return'
    - existence of yolo_label 'camera'
    - x-axis of yolo_label 'sorting'

  - video:

    - aspect ratio of a frame
    - existence of yolo_label 'next vedio'
    - existence of ocr_detection '聊天'
    - existence of ocr_detection '回覆'
    - x-axis of yolo_label 'sorting'

- sub scene recognition:

  - comment:
    
    - home: existence of ocr_detection '貼文'
    - shorts: existence of ocr_detection '留言'
    - video: existence of ocr_detection '留言' or '回覆'
  
  - video action:
    - video: existence of yolo_label 'next vedio'

[Further details click me!](
https://docs.google.com/presentation/d/1b6tTtCOAi0r2IhhoHo_NOOcfNV69BFIdo2rJPLt6b84/edit?usp=sharing)


## Labels

- `home`

  <div style="display: flex; gap: 1rem">
    <img src="https://i.imgur.com/0Yar88i.png" alt="instagram-nav-light" height="50" />
  </div>

- `camera`

  <div style="display: flex; gap: 1rem">
    <img src="https://i.imgur.com/Zg4dwbs.png" alt="instagram-bookmark-light" height="50" />
  </div>

- `return`

  <div style="display: flex; gap: 1rem">
    <img src="https://i.imgur.com/xSChuGq.png" alt="instagram-bookmark-light" height="50" />
  </div>

- `comment`

  <div style="display: flex; gap: 1rem">
    <img src="https://i.imgur.com/PxLHhwo.png" alt="instagram-bookmark-light" height="50" />
  </div>

- `3 dots`

  <div style="display: flex; gap: 1rem">
    <img src="https://i.imgur.com/ooFQraf.png" alt="instagram-logo-light" height="50" />
  </div>

- `next vedio`

  <div style="display: flex; gap: 1rem">
    <img src="https://i.imgur.com/11ourxa.png" alt="instagram-message-light" height="50" />
  </div>
