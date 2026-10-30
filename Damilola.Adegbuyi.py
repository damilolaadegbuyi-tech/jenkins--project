from datetime import datetime

APP_VERSION = "3.0"


def main():
    print("=" * 50)
    print("Hello from Damilola Adegbuyi's Jenkins CI/CD project!")
    print(f"App version: {APP_VERSION}")
    print(f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("This app was built into a Docker image by Jenkins")
    print("and pushed to Docker Hub automatically.")
    print("=" * 50)


if __name__ == "__main__":
    main()
