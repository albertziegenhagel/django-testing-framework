import os
import sys
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--force', action='store_true',
                    help='Do not ask for permission to delete an existing database. Just delete it.')
parser.add_argument('--db', type=str, default='demo',
                    help='The database to put the demo data into. Can be "demo" or "main".')
args = parser.parse_args()

root_path = os.path.dirname(os.path.realpath(__file__))

manage_script_path = os.path.join(root_path, "manage.py")

if args.db == "demo":
    db_file_name = "demo-db.sqlite3"
elif args.db == "main":
    db_file_name = "db.sqlite3"
else:
    print(f"Unknown database '{args.db}'. Has to be 'demo' or 'main'.")
    exit(-1)

db_path = os.path.join(root_path, db_file_name)

if os.path.exists(db_path):
    print("WARNING: found existing database at:")
    print("  {}".format(db_path))

    if args.force:
        print("Deleting file due to --force being used.")
    else:
        print("Proceeding will delete all data in that file.")
        print("Are you sure you want to continue? [Y/n]")
        answer = sys.stdin.read(1)
        if answer != 'Y' and answer != 'y':
            exit(0)

    os.remove(db_path)

os.environ["DTF_ENABLE_WEBHOOKS"] = "0"

subprocess.run(
    [sys.executable, manage_script_path, "migrate", "--database", args.db],
    check=True,
    cwd=root_path,
)

# Users:
# - Name: root PW: test1234
# - Name: demo PW: demopassword
for fixture in ("demo-user", "demo-project", "demo-submissions", "demo-webhook-log"):
    subprocess.run(
        [sys.executable, manage_script_path, "loaddata", "--database", args.db, fixture],
        check=True,
        cwd=root_path,
    )
