from commands import COMMANDS
from cli import create_cli_parser, parse_config_file
from argparse import Namespace


if __name__ == '__main__':
    parser = create_cli_parser()
    args = parser.parse_args()

    if hasattr(args, 'config') and args.config == 'file':
        config_args = parse_config_file(args.config_file)
        args = Namespace(**vars(args), **vars(config_args))

    cmd = COMMANDS[args.command]
    cmd(args)