def convert():
    import sys, os, glob, shutil, tarfile
    import json_to_csv, generate_tfrecord, parse_meta

    outputpath = '/opt/ml/input/data/training'
    shutil.rmtree(outputpath+'/out', ignore_errors=True)
    os.mkdir(outputpath+'/out')
    os.mkdir(outputpath+'/tmp')

    tar_file = glob.glob(outputpath+"/*.tar")[0]
    print(tar_file)
    shutil.copy(tar_file, outputpath+'/data.tar')

    tar_file = tarfile.open(outputpath+'/data.tar')
    tar_file.extractall(outputpath+'/out/') # specify which folder to extract to
    tar_file.close()

    json_to_csv.main()

    generate_tfrecord.main(outputpath+'/tmp/train.csv',outputpath+'/train.record')

    generate_tfrecord.main(outputpath+'/tmp/eval.csv',outputpath+'/eval.record')

    parse_meta.main(outputpath+'/map.pbtxt')

    print(".\nRecords generated")