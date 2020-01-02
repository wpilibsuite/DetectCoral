import argparse

if __name__ == "__main__":
    # Prints "/work/video." and the extension of the original video
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True)
    args = parser.parse_args()
    ext = args.file
    ext = ext[ext.rfind('.'):]
    #ext = ext[2:]
    print("/work/video"+ext)
