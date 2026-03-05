import argparse
from app.models.taskmodel import TaskStatus
from app.services.taskservice import TaskService

def main():
    service = TaskService()
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    add_parser = subparsers.add_parser("add", help="Adds new task")
    add_parser.add_argument("description", type=str, help="Görev açıklaması")

    update_parser = subparsers.add_parser("update", help="Updates task status")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("status", type=str, choices=[s.value for s in TaskStatus], 
                               help="New status (todo, in-progress, done)")

    list_parser = subparsers.add_parser("list", help="Görevleri listeler")
    list_parser.add_argument("--status", type=str, choices=[s.value for s in TaskStatus], 
                             help="Filter tasks by their status")


    delete_parser = subparsers.add_parser("delete", help="Deletes task by given ID")
    delete_parser.add_argument("id", type=int, help="Task ID")

    args = parser.parse_args()

    if args.command == "add":
        try:
            service.add_task(args.description)
        except Exception as e:
            print(f"ERROR!!! Task could't generated: {e}")
    elif args.command == "update":
        service.update_task_status(args.id, TaskStatus(args.status))
    elif args.command == "list":
        service.list_tasks(args.status)
    elif args.command == "delete":
        service.delete_task(args.id)
    else:
        parser.print_help()

