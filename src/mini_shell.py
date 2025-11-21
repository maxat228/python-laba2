import os
from log_setup import setup_logging
from command_ls import ls
from command_cd import cd
from command_cat import cat
from command_cp import cp
from command_mv import mv
from command_rm import rm

def main():
    setup_logging()
    print("Mini Shell started. Type 'exit' to quit.")

    while True:
        try:
            user_input = input(f"{os.getcwd()} $ ").strip()
            if not user_input:
                continue

            command, args = parse_command(user_input)

            if command == "exit":
                break
            elif command == "ls":
                detailed = "-l" in args
                path = None
                for arg in args:
                    if arg != "-l":
                        path = arg
                        break
                ls(path, detailed)
            elif command == "cd":
                if len(args) != 1:
                    print("cd: need exactly one argument")
                else:
                    cd(args[0])
            elif command == "cat":
                if len(args) != 1:
                    print("cat: need exactly one argument")
                else:
                    cat(args[0])
            elif command == "cp":
                recursive = "-r" in args
                sources = [arg for arg in args if arg != "-r"]
                if len(sources) != 2:
                    print("cp: need source and destination")
                else:
                    cp(sources[0], sources[1], recursive)
            elif command == "mv":
                if len(args) != 2:
                    print("mv: need source and destination")
                else:
                    mv(args[0], args[1])
            elif command == "rm":
                recursive = "-r" in args
                targets = [arg for arg in args if arg != "-r"]
                if len(targets) != 1:
                    print("rm: need exactly one target")
                else:
                    rm(targets[0], recursive)
            else:
                print(f"Unknown command: {command}")

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit")
        except Exception as e:
            print(f"Unexpected error: {e}")


# Парсинг введенной пользователем команды
def parse_command(user_input):
    parts = user_input.strip().split()
    if not parts:
        return None, []
    command, args = parts[0], parts[1:]
    return command, args


if __name__ == "__main__":
    main()
