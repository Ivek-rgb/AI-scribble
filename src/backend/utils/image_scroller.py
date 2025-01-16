import tkinter
from PIL import ImageTk
from utils.neural_networks.data_prep import DataLoader

class ImageScroller:

    def __init__(self):
        self.imageScroller = tkinter.Tk()
        self.imageScroller.title("Image Scroller")
        data_test_loader = DataLoader('../../data/training-set/doodles_data/')
        data_test_loader.load_data_npy_dir(None, 100, 10, False)
        self.data, self.labels = data_test_loader.return_split_data_labels(False)
        self.currentIndex = 0
        self.image = self.load_image(self.data[self.currentIndex])
        self.image_label = tkinter.Label(self.imageScroller, image=self.image)
        self.image_label.pack()
        self.label_div = tkinter.Label(self.imageScroller, text=self.labels[0])
        self.label_div.pack()
        self.prev_button = tkinter.Button(self.imageScroller, text="<", command=self.prev_image)
        self.prev_button.pack(side="left", padx=10, pady=10)

        self.next_button = tkinter.Button(self.imageScroller, text=">", command=self.next_image)
        self.next_button.pack(side="right", padx=10, pady=10)
        self.imageScroller.mainloop()


    def load_image(self, data_item):
        image = DataLoader.visualize_array(data_item)
        image = image.resize((400, 400))
        return ImageTk.PhotoImage(image)

    def update_image(self):
        self.image = self.load_image(self.data[self.currentIndex])
        self.image_label.configure(image=self.image)
        self.label_div.configure(text=self.labels[self.currentIndex])

    def next_image(self):
        if self.currentIndex < len(self.data) - 1:
            self.currentIndex += 1
            self.update_image()

    def prev_image(self):
        if self.currentIndex > 0:
            self.currentIndex -= 1
            self.update_image()

