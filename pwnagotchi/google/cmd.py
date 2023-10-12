# Handles the commandline stuff

import pydrive2
from pydrive2.auth import GoogleAuth
import logging


def add_parsers(subparsers):
    """
    Adds the plugins subcommand to a given argparse.ArgumentParser
    """
    #subparsers = parser.add_subparsers()
    # pwnagotchi google
    parser_google = subparsers.add_parser('google')
    google_subparsers = parser_google.add_subparsers(dest='googlecmd')

    # pwnagotchi plugins search
    parser_google_auth = google_subparsers.add_parser('auth', help='Google Authentication')
    parser_google_auth.add_argument('bool', type=bool, help="This will start the authentication process")

    return parser


def used_google_cmd(args):
    """
    Checks if the plugins subcommand was used
    """
    return hasattr(args, 'googlecmd')


def handle_cmd(args):
    """
    Parses the arguments and does the thing the user wants
    """
    if args.plugincmd == 'auth':
        return auth(args.bool)
    elif args.plugincmd == 'refresh':
        return refresh(args)
    raise NotImplementedError()


def auth(args):
    if args == "true":
        # start authentication process
        user_input = input("By completing these steps you give pwnagotchi access to your personal Google Drive!\n"
                           "Personal credentials will be stored only locally for automated verification in the future.\n"
                           "No one else but you have access to these.\n"
                           "Do you agree? \n\n[y(es)/n(o)]")
        if user_input.lower() in ('y', 'yes'):
            try:
                gauth = GoogleAuth(settings_file="settings.yaml")
                print(gauth.GetAuthUrl())
                user_input = input("Please copy this URL into a browser, "
                                   "complete the verification and then copy/paste the code from addressbar.")
                gauth.Auth(user_input)
                gauth.SaveCredentialsFile("credentials.json")
            except Exception as e:
                logging.error(f"Error: {e}")
    return 0


def refresh(args):
    if int(args):
        # refresh token for x amount of time (seconds)
        gauth = GoogleAuth(settings_file="settings.yaml")
        try:
            # Try to load saved client credentials
            gauth.LoadCredentialsFile("credentials.json")
        except pydrive2.auth.InvalidCredentialsError:
            print(gauth.GetAuthUrl())
            user_input = input("Please copy this URL into a browser, "
                               "complete the verification and then copy/paste the code from addressbar.")
            gauth.Auth(user_input)

        if gauth.access_token_expired:
            if gauth.credentials is not None:
                try:
                    # Refresh the token
                    gauth.Refresh()
                except pydrive2.auth.RefreshError:
                    print(gauth.GetAuthUrl())
                    user_input = input("Please copy this URL into a browser, "
                                       "complete the verification and then copy/paste the code from addressbar.")
                    gauth.Auth(user_input)
            else:
                print(gauth.GetAuthUrl())
                user_input = input("Please copy this URL into a browser, "
                                   "complete the verification and then copy/paste the code from addressbar.")
                gauth.Auth(user_input)
        gauth.Authorize()
        gauth.SaveCredentialsFile("credentials.json")
        print("No refresh is required.")
    return 0
