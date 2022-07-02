import os

class DBConfigurations:
    postgres_username = "user"
    postgres_password = "password"
    postgres_port = 5432
    postgres_db = "model_db"
    postgres_server = "localhost"
    sql_alchemy_database_url = (
        f"postgresql://{postgres_username}:{postgres_password}@{postgres_server}:{postgres_port}/{postgres_db}"
    )


class APIConfigurations:
    title = os.getenv("API_TITLE", "Model_DB_Service")
    description = os.getenv(
        "API_DESCRIPTION", "machine learning system training patterns")
    version = os.getenv("API_VERSION", "0.1")


class MachineLearningConfigurations:
    model_dir = r'/Users/User/pytorch-CycleGAN-and-pix2pix/pytorch-CycleGAN-and-pix2pix'
    test_dir = os.path.join(model_dir, r'datasets/facades2/test/')
    train_dir = os.path.join(model_dir, r'datasets/facades2/train/')
    val_dir = os.path.join(model_dir, r'datasets/facades2/val/')
    result_dir = os.path.join(
        model_dir, r"results/facades_pix2pix2/")
    python_dir = 'C:\\JupyterLab\\resources\\jlab_server\\envs\\PyTorch\\python.exe '
    paths = {
        "test": test_dir,
        "train": train_dir,
        "result": result_dir,
        "val": val_dir
    }

class IndicatorConfigurations:
    st1 = 180
    ed1 = 192
    st2 = 192
    ed2 = 204
