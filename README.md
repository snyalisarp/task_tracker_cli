## Task Tracker CLI Tool

A basic task tracker application that store tasks into a json file.

Builded with OOP concepts and seperation of concerns to understanding those concepts better.

Project is dependency free (including the tests) and its build with python version 3.13

Example usage 

- Getting help 

(on Windows)
```bash
python main.py -h
```

(on Linux/macOS)
```bash
python3 main.py -h
```

- Adding task

(on Windows)
```bash
python main.py add "<task_description>"
```

(on Linux/macOS)
```bash
python3 main.py add "<task_description>"
```


- Updating task status

(on Windows)
```bash
python main.py update id <task_id> status ("todo", "in-progress", "done")
```

(on Linux/macOS)
```bash
python3 main.py update id <task_id> status ("todo", "in-progress", "done")
```

- List tasks

(on Windows)
```bash
python main.py list
```

(on Linux/macOS)
```bash
python3 main.py list
```

- List tasks by status

(on Windows)
```bash
python main.py list --status ("todo", "in-progress", "done")
```

(on Linux/macOS)
```bash
python3 main.py list --status ("todo", "in-progress", "done")
```


- Deleting tasks

(on Windows)
```bash
python main.py delete <task_id>
```

(on Linux/macOS)
```bash
python3 main.py delete <task_id>
```

- To run the tests go to projects root directory and type the following command in your terminal

(on Windows)

```bash
python -m unittest discover tests
```

(on Linux/macOS)

```bash
python3 -m unittest discover tests
```