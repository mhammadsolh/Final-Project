# Final-Project
A python script to remove the watermark from a PDF file. The script is used as follow :
Takes the name of the PDF file as command line parameter. 
Takes an optional resolution parameter.
Creates and saves a new PDF file (with the specified resolution) without the watermark.
The Steps:
1-Convert the PDF file into images and save them.
2-Convert each image into 2D array of pixels (matrix).
3-Find specific pixels of the watermark (by color value) and change them into white.
4-Save the modified images.
5-Merge images into a new PDF .
6-Delete images created
