from argparse import ArgumentParser
from dataclasses import dataclass
import importlib
from pathlib import Path
import runpy
from typing import Iterable


SNIPPETS_ROOT = Path(__file__).parent


def path_to_module(path: Path) -> str:
    return path.with_suffix('').as_posix().replace('/', '.')


EXAMPLES: dict[str, Path] = {
    path_to_module(file.relative_to(SNIPPETS_ROOT.parent)): file
    for dir in SNIPPETS_ROOT.glob('*') if dir.is_dir()
    for file in dir.glob('*.py')
}


def create_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog='poetry run python -m snippets',
        description='Runs a snippet',
    )
    parser.add_argument(
        '--lab', '-l', 
        help='Select the index of the lab from which to pick an example',
    )
    parser.add_argument(
        '--example', '-e',
        help='Select the index of the example to run',
    )
    return parser


def run_python_module(name: str):
    return importlib.import_module(name)


@dataclass(frozen=True)
class Example:
    name: str
    path: Path

    @property
    def module(self) -> str:
        print('# Loading module', self.name, 'from', self.path)
        return importlib.import_module(self.name)
    
    def run(self):
        print('# Running module', self.name, 'from', self.path)
        runpy.run_module(self.name)


def find_examples(lab: int, example: int) -> Iterable[Example]:
    for name, path in EXAMPLES.items():
        if name.startswith('snippets.lab' + (lab or "")):
            if f'.example{example or ""}' in name:
                yield Example(name, path)
