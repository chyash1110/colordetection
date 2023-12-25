import cv2
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)
img_path = None
img = None
display_img = None
clicked = False
r = g = b = xpos = ypos = 0

def open_image():
    global img_path
    img_path = filedialog.askopenfilename()
    if img_path:
        update_image()

def update_image():
    global img_path, img_label, img, display_img
    # Read the image
    global img
    img = cv2.imread(img_path)
    if img is not None:
        target_size = (800, 600)
        img = cv2.resize(img, target_size)
        display_img = img.copy()
        pil_img = Image.fromarray(display_img)
        pil_img = ImageTk.PhotoImage(pil_img)
        img_label.config(image=pil_img)
        img_label.image = pil_img
        global clicked, r, g, b
        clicked = False
        r = g = b = 0

def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked, display_img
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        xpos = x
        ypos = y
        b, g, r = display_img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

def open_cv_update():
    global img, clicked, r, g, b, display_img

    if img is not None and img.shape[0] > 0 and img.shape[1] > 0:
        cv2.imshow("Color Detection", display_img)

        if clicked:
            cv2.rectangle(display_img, (20, 20), (750, 60), (b, g, r), -1)
            text = f'Color: RGB({r}, {g}, {b}), Name: {get_color_name(r, g, b)}'
            cv2.putText(display_img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
            if r + g + b >= 600:
                cv2.putText(display_img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
            clicked = False

    if cv2.waitKey(1) == 27: 
        cv2.destroyAllWindows()
    root.after(1, open_cv_update)

def get_color_name(R, G, B):
    minimum = 10000
    color_name = ""
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            color_name = csv.loc[i, "color_name"]
    return color_name
root = tk.Tk()
root.title("Color Detection")
root.geometry("800x600") 
open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack(pady=20)
img_label = tk.Label(root, width=800, height=600)
img_label.pack()
cv2.namedWindow('Color Detection', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Color Detection', 800, 600)
cv2.setMouseCallback('Color Detection', draw_function)
root.after(1, open_cv_update)
root.mainloop()
