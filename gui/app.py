import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import sys


# Access parent folder files
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from similarity_search import search_similar_image


selected_image = None


# Display image in GUI
def display_image(image_path, label):

    img = Image.open(image_path)
    img = img.resize((250, 250))

    photo = ImageTk.PhotoImage(img)

    label.config(image=photo)
    label.image = photo



# Select input image
def browse_image():

    global selected_image

    selected_image = filedialog.askopenfilename(
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png")
        ]
    )

    if selected_image:

        display_image(
            selected_image,
            input_image_label
        )

        input_status.config(
            text="Input Image Selected"
        )



# Search similar image
def search_image():

    if selected_image is None:

        messagebox.showwarning(
            "Warning",
            "Please select an image first"
        )

        return


    result = search_similar_image(
        selected_image
    )


    if result is not None:

        best_image_path = result[0]["image_path"]
        distance = result[0]["distance"]

        print("IMAGE PATH:",best_image_path)
        print("DISTANCE:",distance)


        display_image(
            best_image_path,
            output_image_label
        )


        output_status.config(
            text=
            "Similar Image:\n"
            + os.path.basename(best_image_path)
            +
            "\nDistance: "
            + str(round(distance, 4))
        )


    else:

        messagebox.showinfo(
            "Result",
            "No similar image found"
        )



# ---------------- GUI Window ----------------

root = tk.Tk()

root.title(
    "Image Similarity Search Using Closest Pair"
)

root.geometry(
    "700x700"
)



title = tk.Label(
    root,
    text="IMAGE SIMILARITY SEARCH",
    font=("Arial",18,"bold")
)

title.pack(
    pady=10
)



# Input Image

tk.Button(
    root,
    text="Select Input Image",
    command=browse_image,
    width=20
).pack()



input_status = tk.Label(
    root,
    text="No Image Selected"
)

input_status.pack()



input_image_label = tk.Label(root)

input_image_label.pack(
    pady=10
)



# Search Button

tk.Button(
    root,
    text="Search Similar Image",
    command=search_image,
    width=25
).pack(
    pady=10
)



# Output Image

output_status = tk.Label(
    root,
    text="No Result",
    font=("Arial",14)
)

output_status.pack()



output_image_label = tk.Label(root)

output_image_label.pack(
    pady=10
)



root.mainloop()