import subprocess

def dwnld_img(url, filename):

  # Create the curl command
  command = ['curl', '-L', '-o', filename, '--insecure', url]

  
  # Run the command using subprocess
  print(command)
  subprocess.run(command)

def remove_file(file_name):
    try:
        subprocess.run(['rm', file_name], check=True)
        print(f"File '{file_name}' successfully removed.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while removing file '{file_name}': {e}")
