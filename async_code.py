import os
import asyncio
import shutil
import logging
from argparse import ArgumentParser
from pathlib import Path


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_args():
    parser = ArgumentParser(description="Sort files by extension")
    parser.add_argument("source_folder", type=str, help="Source folder")
    parser.add_argument("output_folder", type=str, help="Output folder")
    return parser.parse_args()


async def read_folder(source_folder, output_folder):
    tasks = []
    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = Path(root) / file
            tasks.append(copy_file(file_path, output_folder))
    await asyncio.gather(*tasks)


async def copy_file(file_path, output_folder):
    try:
        ext = file_path.suffix[1:]
        target_dir = Path(output_folder) / ext
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / file_path.name
        await asyncio.to_thread(shutil.copy, file_path, target_path)
        logger.info(f"Copied {file_path} to {target_path}")
    except Exception as e:
        logger.error(f"Error copying {file_path}: {e}")


async def main():
    args = parse_args()
    source_folder = Path(args.source_folder)
    output_folder = Path(args.output_folder)
    await read_folder(source_folder, output_folder)

if __name__ == "__main__":
    asyncio.run(main())
