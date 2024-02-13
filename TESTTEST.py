import telepot
from telepot.loop import MessageLoop
from instagrapi import Client
import requests
from PIL import Image
import os

TOKEN = '6813181139:AAFbAHnFwUVk6rBy5jQMznoVEvogP-0SMw0'
cl = Client()
media_ids = set()  # Use a set to store unique file IDs

def download_image(url, file_path):
    response = requests.get(url, stream=True)
    with open(file_path, 'wb') as f:
        # f.write(response.content)
        img = Image.open(response.raw)
        img = img.resize((1080, 1080))
        img.save(file_path)

def generate_unique_filename(base_filename):
    extension = ".jpg"
    # Ensure the extension starts with a dot (e.g., ".jpg")
    if not extension.startswith("."):
        extension = "." + extension

    # Initialize the counter
    i = 1
    new_file_name = f"{base_filename}{i}{extension}"

    # Check if the file exists, incrementing the counter if needed
    while os.path.exists(new_file_name):
        i += 1
        new_file_name = f"{base_filename}{i}{extension}"

    return new_file_name
def upload_post(photo_url, caption):
    cl.login("autotelepost", "autotelepost456")

    downloaded_image_path = generate_unique_filename("downloaded_image")
    download_image(photo_url, downloaded_image_path)
    # media = cl.photo_upload(downloaded_image_path, caption)
    media_ids.add(downloaded_image_path)  # Add the file ID to the set
    # os.remove(downloaded_image_path)  # Cleanup: Delete the downloaded image

def process_after_all_images():
    # Your code to run after all images are processed

    print("Processing after all images...", media_ids)
    if media_ids:
        cl.album_upload(media_ids, "Hello")

def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'photo':
        # Handle photo messages
        photo_array = msg['photo']
        file_id = photo_array[-1]['file_id']
        print(f"Received photo with file_id: {file_id}")

        # Get the caption of the photo
        caption = msg.get('caption', '')
        print(f"Caption: {caption}")

        # getting the photoURL
        file_info = bot.getFile(file_id)
        file_path = file_info['file_path']
        photo_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
        print(photo_url)

        upload_post(photo_url, caption)

        # Check if all images in the message are processed
        if all_images_processed(msg):
            process_after_all_images()  # Call the function after processing all images
            media_ids.clear()  # Clear the set for the next message
            delete_files()

# Create the bot instance
bot = telepot.Bot(TOKEN)

# Function to check if all images in the message are processed
def all_images_processed(msg):
    photo_array = msg.get('photo', [])
    print(photo_array)
    expected_image_count = len(photo_array)
    print(expected_image_count)
    return len(media_ids) == expected_image_count

def delete_files():
    directory_path = "C:/Users/User/Documents/121 submission/ProjectOne"
    prefix = "downloaded_image"
    for filename in os.listdir(directory_path):
        if filename.startswith(prefix):
            file_path = os.path.join(directory_path, filename)
            os.remove(file_path)

# Set up the message handler
MessageLoop(bot, handle_message).run_as_thread()

print('Bot is listening...')

# Keep the program running
while True:
    pass
