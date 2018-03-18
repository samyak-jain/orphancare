import cv2
from darkflow.net.build import TFNet
import matplotlib.pyplot as plt
import numpy as np

options = {
    'model': '/home/apurvnit/Projects/darkflow/cfg/yolo.cfg',
    'load': '/home/apurvnit/Projects/darkflow/bin/yolo.weights',
    'label': '/home/apurvnit/Projects/darkflow/cfg/coco.names',
    'threshold': 0.3,
    'gpu': 0.8
}

tfnet = TFNet(options)

img = cv2.imread('/home/apurvnit/Projects/codespace-backend/utility/test/surya.jpeg',cv2.IMREAD_COLOR)
print(type(img))

result = tfnet.return_predict(np.array(img))

tl = (result[0]['topleft']['x'], result[0]['topleft']['y'])
br = (result[0]['bottomright']['x'], result[0]['bottomright']['y'])

label = result[0]['label']
img = cv2.rectangle(img, tl, br, (255,0,0), 7)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.putText(img, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
plt.imshow(img)
plt.show()
