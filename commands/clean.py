from os import path, listdir, unlink
import shutil
from utils.fileutils import get_output_dir, get_cache_dir

def clean(args):
    clean_output(args.id)
    clean_cache()

def clean_output(simulation_id: str):
    output_dir = get_output_dir(simulation_id)
    delete_content_in_dir(output_dir)


def delete_content_in_dir(dir: str):    
    for filename in listdir(dir):
        file_path = path.join(dir, filename)
        try:
            if path.isfile(file_path) or path.islink(file_path):
                unlink(file_path)
            elif path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete {} due to {}'.format(file_path, e))


def clean_cache():
    cache_dir = get_cache_dir()
    delete_content_in_dir(cache_dir)