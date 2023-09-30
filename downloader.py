import requests
import os
import io
import pypdf
from PIL import Image
from tqdm import tqdm

def download_ebooks():
    # Define the URL of the web page containing the images
    url = "http://readonline.ebookstou.org/flipbook/"+ input("Enter five digits:") + "/files/mobile/"

    # Define the output PDF file name
    output_pdf_file = input("Enter File Name:") + ".pdf"

    # Create a PDF file with pypdf
    pdf = pypdf.PdfWriter()

    # Parse the HTML content to find image URLs (you might need to use a proper HTML parsing library)
    # For simplicity, let's assume you have a list of image URLs called 'image_urls'
    page_num = int(input("Enter the last page number:"))
    load_bar = tqdm(total=page_num)
    image_urls = [url + str(i) + ".jpg" for i in range(1, page_num + 1)]
    current_directory = os.getcwd()
    temp_directory = os.path.join(current_directory, "temp")

    # Create the temporary directory if it doesn't exist
    if not os.path.exists(temp_directory):
        os.makedirs(temp_directory)

    # Loop through each image URL and add it to the PDF
    for index, image_url in enumerate(image_urls):
            
        # Send a GET request to download the image
        image_response = requests.get(image_url)

        # Check if the request was successful
        if image_response.status_code == 200:
            # Open the image as a binary stream
            image_bytes = io.BytesIO(image_response.content)

            # Open the image using PIL (Python Imaging Library)
            img = Image.open(image_bytes)
            img_filename = str(index) + ".pdf"
            img_path = os.path.join(temp_directory, img_filename)

            # Convert and save the image as a PDF
            img.save(img_path, "PDF")

            # Read the saved PDF page and add it to the main PDF
            page = pypdf.PdfReader(img_path).pages[0]
            pdf.add_page(page)
            load_bar.update(1)

    load_bar.close()

    # Save the combined PDF to the current path
    output_pdf_path = os.path.join(current_directory, output_pdf_file)
    with open(output_pdf_path, "wb") as pdf_output:
        pdf.write(pdf_output)

    # Clean up temporary PDF files
    for tempfile in os.listdir(temp_directory):
        temp_file_path = os.path.join(temp_directory, tempfile)
        os.remove(temp_file_path)

    # Remove the temporary directory
    os.rmdir(temp_directory)

    print(f"PDF created: {output_pdf_file}")

while True:
    if input("Continue (Y/n):") != "y":
        break
    download_ebooks()

