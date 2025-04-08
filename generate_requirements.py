import subprocess

def save_requirements():
    with open("requirements.txt", "w") as f:
        reqs = subprocess.check_output(["pip", "freeze"]).decode("utf-8")
        f.write(reqs)

if __name__ == "__main__":
    save_requirements()
    print("Requirements saved to requirements.txt")
    print("You can now install the requirements using:\n\npip install -r requirements.txt")