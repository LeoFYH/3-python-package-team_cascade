from . import start_session, end_session, get_status, reset_pet
from .data_manager import load_state, save_state
from .pet import rename_pet, collect_money, feed_pet, check_daily_mood_decay
import argparse
import study_pet.tracker as tracker


def main():
    parser = argparse.ArgumentParser(description="🐾 StudyPet CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Start command
    subparsers.add_parser("start", help="Start a study session")
    
    # End command
    subparsers.add_parser("end", help="End current study session")
    
    # Status command
    subparsers.add_parser("status", help="Check pet status")
    
    # Feed command
    feed_parser = subparsers.add_parser("feed", help="Feed your pet")
    feed_parser.add_argument(
        "--food-type",
        choices=["apple", "cake", "coffee", "carrot", "sushi", "custom"],
        help="Food type to feed directly (optional, shows menu if not provided)",
    )
    
    # Collect command
    collect_parser = subparsers.add_parser("collect", help="Collect coins")
    collect_parser.add_argument(
        "--force",
        action="store_true",
        help="Force collection, bypass cooldown (for testing)",
    )
    
    # Rename command
    rename_parser = subparsers.add_parser("rename", help="Rename your pet")
    rename_parser.add_argument(
        "--name",
        help="New name for your pet (optional, will prompt if not provided)",
    )
    
    # Menu command (default)
    subparsers.add_parser("menu", help="Open interactive menu")
    
    args = parser.parse_args()
    
    # Default to menu if no command provided
    if not args.command:
        args.command = "menu"

    check_daily_mood_decay()

    if args.command == "start":
        start_session()
    elif args.command == "end":
        end_session()
    elif args.command == "status":
        print(get_status())
    elif args.command == "feed":
        feed_pet(food_type=getattr(args, 'food_type', None))
    elif args.command == "collect":
        collect_money(force=getattr(args, 'force', False))
    elif args.command == "rename":
        rename_pet(new_name=getattr(args, 'name', None))
    elif args.command == "menu":
        main_menu()
    else:
        parser.print_help()


def actions_menu():
    """Submenu for all pet-related actions."""
    while True:
        print("\nActions Menu:")
        print("1. Collect coins ")
        print("2. Feed your pet")
        print("3. Back")

        choice = input("\nSelect an option (1–3): ").strip()

        if choice == "1":
            collect_money()
        elif choice == "2":
            feed_pet()
        elif choice == "3":
            break
        else:
            print("Invalid option. Try again.")


def settings_menu():
    """Submenu for settings and info."""
    while True:
        print("\nSettings Menu:")
        print("1. Check pet status")
        print("2. Rename your pet")
        print("3. Reset all data")
        print("4. Back")

        choice = input("\nSelect an option (1–4): ").strip()

        if choice == "1":
            print(get_status())
        elif choice == "2":
            rename_pet()
        elif choice == "3":
            confirm = input(
                "This will reset all progress. Type 'byebye' to confirm "
            ).lower()
            if confirm == "byebye":
                reset_pet()
        elif choice == "4":
            break
        else:
            print("Invalid option. Try again.")


def main_menu():
    """Main entry menu."""
    while True:
        print("\n🐾 Welcome to StudyPet!\n")
        print("1. Start studying ")
        print("2. End session")
        print("3. Actions")
        print("4. Settings")
        print("5. Close Menu (return to terminal)")
        print("6. Exit (Close StudyPet to terminal)")

        choice = input("\nSelect an option (1–6): ").strip()
        if choice == "1":
            start_session()
        elif choice == "2":
            end_session()
        elif choice == "3":
            actions_menu()
        elif choice == "4":
            settings_menu()
        elif choice == "5":
            tracker.manual_close = True
            break
        elif choice == "6":
            tracker.manual_close = False
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
