"""
Specifies general helpers thorough the project
"""
from PIL import Image
import pytesseract
import requests
import discord
import time
import io

class DiscordUserHelper:
    
    def __init__(self, id, username, discriminator, time):
        self.id = id
        print(f"HASH VALUE - {hash(self.id)}")
        self.username = username
        self.discriminator = discriminator
        self.time = time
        self.solution_path = ''

        self.username_complete = f'{self.username}#{self.discriminator}'
    
    def is_time_question_expired(self, min = 20):
        """
        Returns a bool indicating if the time of the current user has expired or not
        """
        return ((time.time() - self.time) / 3600) >= min
    
    def validate_solution(self):
        image_helper = ImageReaderHelper()
        content = image_helper.read_image_content_from_url(self.solution_path)
        print(content)
        # validate if solution was right ...

    def __hash__(self):
        return self.username_complete
        

class DiscordMessageHelper:
    """
    Helper that creates a layer of abstraction over message sending
    """

    @classmethod
    async def send_message_embed(cls, channel, title, content):
        """
        Abstraction layer that creates an embed and sends a message
        """        
        embed = discord.Embed(title=title, description=content)
        await channel.send(embed=embed)
    
    @classmethod
    async def send_message(cls, channel, msg): 
        """
        Sends a common message
        """
        await channel.send(msg)


class ImageReaderHelper:

    def __init__(self):
        self.__initialize_pytesseract()

    def __initialize_pytesseract(self):
        """
        Initializes pytesseract program and all of its dependencies

        IMPORTANT: change program path if such project will be executed on other machine!
        """

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

    def read_image_content_from_file(self, path):
        return pytesseract.image_to_string(image)
    
    def read_image_content_from_url(self, url_path):
        response = requests.get(url_path)
        image = Image.open(io.BytesIO(response.content))
        return pytesseract.image_to_string(image)
    

if __name__ == "__main__":
    image_helper = ImageReaderHelper()
    content = image_helper.read_image_content_from_url('https://ericleads.files.wordpress.com/2012/10/whiteboard-code.jpg')
    print(content)