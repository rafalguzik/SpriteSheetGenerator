from PIL import Image
import os, math, time, sys
max_frames_row = 10.0
frames = []
tile_width = 0
tile_height = 0

spritesheet_width = 0
spritesheet_height = 0

frame_dir = sys.argv[1]

files = os.listdir(frame_dir)
files.sort()
print(files)

for current_file in files :
    try:
        with Image.open(frame_dir + current_file) as im :
            frames.append(im.getdata())
    except:
        print(current_file + " is not a valid image")

tile_width = frames[0].size[0]
tile_height = frames[0].size[1]
crop = 0
resize = False

if len(sys.argv) > 3:
    tile_width = int(sys.argv[2])
    tile_height = int(sys.argv[3])
    resize = True

if len(sys.argv) > 4:
    crop = int(sys.argv[4])



if len(frames) > max_frames_row :
    spritesheet_width = tile_width * max_frames_row
    required_rows = math.ceil(len(frames)/max_frames_row)
    spritesheet_height = tile_height * required_rows
else:
    spritesheet_width = tile_width*len(frames)
    spritesheet_height = tile_height
    
print(spritesheet_height)
print(spritesheet_width)

spritesheet = Image.new("RGBA",(int(spritesheet_width), int(spritesheet_height)))

for current_frame in frames :
    top = tile_height * math.floor((frames.index(current_frame))/max_frames_row)
    left = tile_width * (frames.index(current_frame) % max_frames_row)
    bottom = top + tile_height
    right = left + tile_width
    
    box = (left,top,right,bottom)
    box = [int(i) for i in box]
    if resize:
        if crop > 0:
            current_frame = current_frame.crop((crop,crop,current_frame.size[0]-crop,current_frame.size[1]-crop))
        cut_frame = current_frame.resize([tile_width, tile_height])
    else:
        cut_frame = current_frame.crop((crop,crop,tile_width-crop,tile_height-crop))
    
    spritesheet.paste(cut_frame, box)
    
spritesheet.save("spritesheet-" + time.strftime("%Y-%m-%dT%H-%M-%S") + ".png", "PNG")
