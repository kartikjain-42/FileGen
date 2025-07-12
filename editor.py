import os

def write_to_file(filepath, data, mode='a'):
    """
    Write or append data to a file at any valid location.
    Automatically creates intermediate directories if needed.
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)  # create directories if needed
        with open(filepath, mode, encoding='utf-8') as f:
            f.write(data + '\n')
        print(f"Data {'written' if mode == 'w' else 'appended'} successfully to {filepath}.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    filepath = input("Enter full file path (e.g., /tmp/log.txt or C:\\Users\\you\\file.txt): ")
    mode = input("Choose mode - write (w) or append (a): ").strip().lower()
    if mode not in ['w', 'a']:
        print("Invalid mode. Defaulting to append.")
        mode = 'a'

    print("Enter data to write (type END to finish):")
    while True:
        line = input()
        if line.strip() == "END":
            break
        write_to_file(filepath, line, mode)
