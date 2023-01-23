# sticker_detection
Identify stickers with text on images of microscopic slides. 
The purpose of this program is to erase patient information to protect their privacy. This program uses computer vision to detect text on a sticker on microscopic slides.

# How to Run
python edge_detect.py

# How it Works
1) Start with a test image
<img width="196" alt="image" src="https://user-images.githubusercontent.com/30853467/214160013-18b1e848-e37b-478d-88ed-c6f73723f822.png">
2)Perform morphological transformation through dilation
<img width="193" alt="image" src="https://user-images.githubusercontent.com/30853467/214160236-35282394-d7ac-4b4b-b549-064fb10b0d67.png">
3)Store all contours present in the image



# Results
<img width="1357" alt="image" src="https://user-images.githubusercontent.com/30853467/214158965-025f8a1d-6d8f-450b-8c41-5e54ff3bbdcd.png">

