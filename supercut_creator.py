import os
import sys

# CONSTANTS
CUT_TIME = 0
LABEL = 4

# FUNCTIOINS
def create_clip(cut_in, cut_out):
    print("Cutting from {} to {}".format(cut_in, cut_out))
    # run an ffmpeg thread to create MP4 clips
    mp4 = 'ffmpeg -i ' + videoFile + ' -ss ' + \
        cut_in + \
        ' -to ' + \
        cut_out + \
        ' -c copy clip' + str(clip_counter) + '.mp4'
    print(mp4)
    os.system(mp4)

# SCRIPT
# Check for the command line inputs
if len(sys.argv) < 2:
    print("No video file or cut file given\nUsage: \
    python supercut_creator.py [videoFile] [cutFile]")
    quit()
else:
    videoFile = sys.argv[1]
    cutFile = sys.argv[2]
print(cutFile, videoFile)

# Open a clip file list for stitching
stitch_file = open("stitch_file.txt", "w")

# Find all the cut points and create the clips
linenum = 0
clip_counter = 0
with open(cutFile, 'r') as f:
    for line in f:
        line = line.strip().split(",")
        if line[LABEL] == "in":
            cut_in = line[CUT_TIME]
        elif line[LABEL] == "out":
            cut_out = line[CUT_TIME]
            create_clip(cut_in, cut_out)
            stitch_file.write("file 'clip{}.mp4'\n".format(clip_counter))
            clip_counter += 1
        else:
            pass
stitch_file.close()

# Stitch the clips together in a supercut
stitch = "ffmpeg -f concat -i stitch_file.txt -c copy supercut.mp4"
os.system(stitch)
