import sys
from PIL import Image, ImageDraw, ImageFont ,ImageOps
import json
import os

def format_string(line_length, input_string):
    words = input_string.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + word) <= line_length:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    if current_line:
        lines.append(current_line.strip())

    formatted_string = "\n".join(lines)
    return formatted_string

def add_blank_slots(json_data):
    blank_indexes = []
    for i in range(len(json_data['segments'])):
        if i+1<len(json_data['segments']):
            if not round(json_data['segments'][i]['end']) == round(json_data['segments'][i+1]['start']):
                blank_indexes.append((i+1, json_data['segments'][i]['end'], json_data['segments'][i+1]['start']))
    count = 0
    for i in range(len(blank_indexes)):
        dict = {}
        dict = dict.fromkeys(json_data['segments'][0].keys())
        dict['start'] = blank_indexes[i][1]
        dict['end'] = blank_indexes[i][2]
        dict['text'] = '...'
        dict['tokens'] = []
        json_data['segments'].insert(blank_indexes[i][0]+count, dict)
        count+=1

def create_image(text, font_size=75, width=1280, height=720, output_path='output', curr_dir=None):
    # Create a blank image with a white background
    if curr_dir == None:
        curr_dir = os.getcwd()
    image = Image.new("RGB", (width, height), color=(147, 64, 136))
    draw = ImageDraw.Draw(image)
    
    # Load a font (you can change the font file path as needed)
    font_path = os.path.join(curr_dir, r'utils\fonts\Dancing_Script', 'DancingScript-VariableFont_wght.ttf')
    font = ImageFont.truetype(font_path, font_size)

    ftext = format_string(40, text)

    draw.text(((width)/2, (height)/2), text=ftext, fill='white', font=font, anchor="mm", align='center')

    # Save the image
    image.save(output_path + '.png')


def text_to_images(song_name):
    curr_dir = os.getcwd()

    # reading the lyrics from the json file(changed by Anish): 
    input_file_path = os.path.join(curr_dir, rf'processed_songs\{song_name}\lyrics\new_{song_name}_Vocals.json')
    with open (input_file_path, 'r') as file:
        json_data = json.load(file)

    song_title = input_file_path.split(sep="\\")[-1].replace(".json","").upper().split("_")[1]
    json_data['title'] = song_title

    add_blank_slots(json_data) # adding blank dictionaries into the json file

    lines = [json_data['segments'][i]['text'] for i in range(len(json_data['segments']))]

    output_folder = os.path.join(curr_dir, rf'processed_songs\{song_name}\lyrics\lyric_images')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each line and create an image
    image_path = os.path.join(output_folder, "output_image_0")
    create_image(json_data['title'], output_path=image_path, curr_dir=curr_dir)
    json_data['image_title_location'] = image_path

    for i, line in enumerate(lines):
        image_path = os.path.join(output_folder, f"output_image_{i+1}")
        json_data['segments'][i]['image_location'] = f"lyrics\\\\lyric_images\\\\output_image_{i+1}" + ".png" #changed by Anish
        create_image(line.strip(), output_path=image_path)
    
    for i in range(len(json_data["segments"])):
        if i ==0:
            json_data['title_duration'] =  float(json_data["segments"][0]['start'])
        json_data["segments"][i]['duration'] = float(json_data["segments"][i]['end']) - float(json_data["segments"][i]['start'])
 
    input_text_path = os.path.join(curr_dir, rf'processed_songs\{song_name}\images_duration.txt')
    with open(input_text_path , "w") as f:
        title_slide = "file " + "lyrics\\\\lyric_images\\\\output_image_0.png" + "\n" + "duration " + str(json_data['title_duration']) + "\n"
        f.write(title_slide)
        for i in range(len(json_data["segments"])):
            buffer = "file " + json_data["segments"][i]['image_location'] + "\n" + "duration " + str(json_data["segments"][i]['duration']) + "\n"
            f.write(buffer)

    # saving the json file: (changed by Anish)
    with open(input_file_path, 'w') as outfile:
        json.dump(json_data, outfile)