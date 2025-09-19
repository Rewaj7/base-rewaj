import argparse
from lib.dummy import dummy_function


def main():
    parser = argparse.ArgumentParser(prog="analyze", description="Analyze CLI tool")
    parser.add_argument(
        "--phrase",
        required=True,
        help="Phrase to echo back"
    )

    args = parser.parse_args()
    phrase = args.phrase
    output = dummy_function(phrase)
    print(output)


if __name__ == "__main__":
    main()