import argparse
import logging
from pathlib import Path
from shutil import copyfile
from threading import Thread, Condition

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

args = vars(parser.parse_args())
source = Path(args.get("source"))
output = Path(args.get("output"))


def master(path: Path) -> None:
    logging.info("grab folder")
    try:
        grab_folder(path)
        with condition:
            condition.notify_all()
    except FileNotFoundError as e:
        logging.error(e)


def grab_folder(path: Path) -> None:
    logging.info("Waiting for Master order...")
    with condition:
        condition.wait()
        for el in path.iterdir():
            if el.is_dir():
                thread = Thread(target=grab_folder, args=(el,))
                thread.start()
            else:
                suffix = el.suffix[1:]
                thread = Thread(target=copy_file, args=(el, output / suffix))
                thread.start()


def copy_file(file: Path, output_folder: Path) -> None:
    try:
        output_folder.mkdir(parents=True, exist_ok=True)
        logging.info(f"copy {file.name} from {file.parent} to {output_folder}")
        copyfile(file, output_folder / file.name)
    except OSError as e:
        logging.error(e)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(threadName)s - %(message)s")
    condition = Condition()

    master_grabs = Thread(target=master, args=(source,))
    master_grabs.start()

    master_grabs.join()
    print("Finished")
