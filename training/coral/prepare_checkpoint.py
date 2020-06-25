import tarfile, os
#this script simply extracts the model into the ckpt directory.
#to avoid downloads within the train script, a switch model script
#may be called before the train script, but the default model is
#downloaded to the research directory upon buiding the image

def prepare_checkpoint(network_type):

    #eventually this will be global dictionary
    ckpt_name_map = {}
    ckpt_name_map["mobilenet_v1_ssd"]="ssd_mobilenet_v1_quantized_300x300_coco14_sync_2018_07_18"
    ckpt_name_map["mobilenet_v2_ssd"]="ssd_mobilenet_v2_quantized_300x300_coco_2019_01_03"
    CKPT_DIR = os.path.join(os.getcwd(),'learn','ckpt')

    modelname = ckpt_name_map[network_type]+'.tar.gz'

    with tarfile.open(modelname) as model:
        model.extractall(CKPT_DIR)

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-net', '--network_type', help='network type', type=str, required=True)
    args = parser.parse_args()
    
    prepare_checkpoint(args.network_type)
