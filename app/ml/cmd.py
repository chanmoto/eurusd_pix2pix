import subprocess
from  ml.pix2pix import rmdir
from configuration import MachineLearningConfigurations as MLConfig


def train(Continue: str):
    cmd = MLConfig.python_dir + "train.py --dataroot ./datasets/facades2 --name facades_pix2pix2 --model pix2pix --batch_size 1 --direction AtoB --gpu_ids 0 --no_flip {}".format(
        Continue)
    subprocess.call(cmd, shell=True, cwd=MLConfig.model_dir)
    return "pix2pix -train was called"


def test(Phase: str,number:int):
    rmdir(MLConfig.paths["result"])
    cmd = MLConfig.python_dir + \
        "test.py --dataroot ./datasets/facades2 --name facades_pix2pix2 --model pix2pix --direction AtoB --phase {} --num_test {}".format(
            Phase,number)
    subprocess.check_output(cmd, shell=True, cwd=MLConfig.model_dir)
    return " pix2pix -test was called"
