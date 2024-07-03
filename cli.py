import os
import subprocess
import sys

ASCII_ART = """
 __          __   _       _                _____  
 \ \        / /  | |     | |         /\   |_   _| 
  \ \  /\  / /_ _| |_ ___| |__      /  \    | |   
   \ \/  \/ / _` | __/ __| '_ \    / /\ \   | |   
    \  /\  / (_| | || (__| | | |_ / ____ \ _| |_  
     \/  \/ \__,_|\__\___|_| |_(_)_/    \_\_____| 
                                                  
                                                  
"""

def run_command(command):
    """Run a system command and print output in real-time."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    for line in iter(process.stdout.readline, b''):
        sys.stdout.write(line.decode('utf-8'))
    process.stdout.close()
    process.wait()

def setup_environment():
    """Set up the Python environment and install dependencies."""
    if not os.path.exists('setup_environment.py'):
        print("setup_environment.py not found.")
        return

    print("Running setup_environment.py...")
    run_command(f"{sys.executable} setup_environment.py")

    print("Building the React frontend...")
    run_command("npm run build")

    domain_name = input("Enter the domain name on which it will be running: ")
    print(f"Application is set up and running at http://{domain_name}")

def list_datasets():
    """List available datasets."""
    datasets = [f for f in os.listdir('datasets') if os.path.isdir(os.path.join('datasets', f))]
    return datasets

def train_dataset():
    """Prompt for dataset directory and start training."""
    data_dir = input("Enter the directory with data to train: ")
    if not os.path.exists(data_dir):
        print("Directory not found.")
        return

    print(f"Training with data from {data_dir}...")
    # Add training logic here

def delete_dataset():
    """List datasets, prompt for selection, and confirm deletion."""
    datasets = list_datasets()
    if not datasets:
        print("No datasets found.")
        return

    print("Available datasets:")
    for i, dataset in enumerate(datasets):
        print(f"{i + 1}. {dataset}")

    choice = int(input("Enter the number of the dataset to delete: "))
    if 1 <= choice <= len(datasets):
        dataset_to_delete = datasets[choice - 1]
        confirm = input(f"Are you sure you want to delete the dataset '{dataset_to_delete}'? (yes/no): ")
        if confirm.lower() == 'yes':
            print(f"Deleting dataset '{dataset_to_delete}'...")
            # Add dataset deletion logic here
        else:
            print("Deletion cancelled.")
    else:
        print("Invalid choice.")

def main():
    while True:
        print(ASCII_ART)
        print("1. Train a dataset")
        print("2. Delete a dataset")
        print("3. Run Watch.AI")
        print("4. Exit")

        choice = input("Enter your choice: ")
        if choice == '1':
            train_dataset()
        elif choice == '2':
            delete_dataset()
        elif choice == '3':
            setup_environment()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
