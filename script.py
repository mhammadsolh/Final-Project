from skimage import io
from PIL import Image
import fitz
import argparse
import numpy as np
import os

# Take pdf filename as command line argument
# Take an optional resolution parameter (exp: 3.62)
parser = argparse.ArgumentParser()
parser.add_argument("--pdf", required=True, type=str)
parser.add_argument("-r", "--resolution", type=float, default=150 / 72)
args = parser.parse_args()

path = os.path.dirname(args.pdf)  # Get the path
filename = os.path.basename(args.pdf)  # Get the filename


# Check if the pixel is grey (belongs to the watermark)
def watermark_pixel(r, g, b):
    if 170 < r < 250 and 170 < g < 250 and 170 < b < 250:
        return True
    else:
        return False


# Create images of all pdf pages
def create_images(pdf):
    print("Creating Images ...")
    pages = fitz.open(pdf)
    pages_names = []
    for i, page in enumerate(pages):
        pic = page.get_pixmap(matrix=fitz.Matrix(args.resolution, args.resolution))  # render page to an image
        pic.save(os.path.join(path, f"page_{i}.png"))
        pages_names.append(os.path.join(path, f"page_{i}.png"))
    print("Images are created ...")
    return pages_names


# Replace all the watermark pixels with white pixels
def handle(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if watermark_pixel(img[i][j][0], img[i][j][1], img[i][j][2]):
                img[i][j][0] = img[i][j][1] = img[i][j][2] = 255
    return img


# Save the pdf file
def save_pdf(images_names):
    print("Merging ...")
    images = []
    image1 = Image.open(images_names[0])
    print("Image 0 is merged ...")
    for i, image_name in enumerate(images_names[1:]):
        image = Image.open(image_name)
        images.append(image)
        print(f"Image {i + 1} is merged ...")
    pdf_name = os.path.join(path, f"no_watermark_{filename}")
    image1.save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=images)
    print("Merging is done !")


# Delete the images after creating the pdf
def delete_images(images_names):
    for i, image_name in enumerate(images_names):
        os.remove(image_name)
        print(f"Image {i} is removed ... ")


def main():
    pages = create_images(args.pdf)  # Create images

    images_list = []

    print("Handling images ...")
    for i, page in enumerate(pages):  # For each page
        image = Image.open(page)  # Open it
        image = np.array(image)  # Transform it to a pixel matrix
        image = handle(image)  # Handel watermark pixels
        io.imsave(os.path.join(path, f"new_page_{i}.png"), image)  # Save the resulting image
        images_list.append(os.path.join(path, f"new_page_{i}.png"))
        print(f"Page {i} processed ...")

    save_pdf(images_list)  # Save the resulting pdf

    delete_images(pages)  # Delete first images
    delete_images(images_list)  # Delete processed images

    print("PDF is ready !")


if __name__ == '__main__':
    main()
#Team
#Mhammad Mazen Solh (212117)
#Mohamad Hadi ALOUTA (213142)
#Khaled Najem (210947)
#Ali Kanso (210923)
