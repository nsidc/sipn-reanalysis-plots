import sys
from pathlib import Path

from invoke import task

from .util import print_and_run

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(PROJECT_DIR)

# WARNING: Do not import from sipn_reanalysis_plots at this level to avoid failure of basic
# commands because unneeded envvars are not populated.


@task(aliases=['flake8'])
def lint(ctx):
    """Run flake8 linting."""
    from sipn_reanalysis_plots.constants.paths import PACKAGE_DIR

    print_and_run(
        f'cd {PROJECT_DIR} && flake8 {PACKAGE_DIR}',
    )

    print('🎉🙈 Linting passed.')


@task
def formatcheck(ctx):
    """Check that the code conforms to formatting standards."""
    print_and_run(f"isort --check-only {PROJECT_DIR}")
    print_and_run(f"black --check {PROJECT_DIR}")

    print("🎉🙈 Format check passed.")


@task(aliases=['mypy'])
def typecheck(ctx):
    """Run mypy static type analysis."""
    from sipn_reanalysis_plots.constants.paths import PACKAGE_DIR

    print_and_run(
        f'cd {PROJECT_DIR} &&'
        f' mypy --config-file={PROJECT_DIR}/.mypy.ini {PACKAGE_DIR}',
    )
    print('🎉🦆 Type checking passed.')


@task(
    pre=[lint, formatcheck, typecheck],
    default=True,
)
def all(ctx):
    """Run all tasks."""
    print('🎉❤️  All tests passed!')
