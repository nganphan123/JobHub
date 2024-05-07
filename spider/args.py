import argparse
from enum import Enum, unique


@unique
class Provider(Enum):
    LINKEDIN = ("linkedin",)
    INDEED = "indeed"


def get_provider(provider, default):
    provider = provider.strip().lower()
    for member in Provider:
        if member.value == provider:
            return member
    return default


def get_arg_parser():
    parser = argparse.ArgumentParser(
        description="Find application job postings based on keywords.",
    )
    parser.add_argument(
        "-p", "--provider", default=Provider.LINKEDIN, help="Job Posting Sites"
    )
    return parser