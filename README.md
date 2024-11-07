-- Quiz Project
This project is a Python-based quiz application that uses data analysis and a structured dataset to create an engaging quiz experience about movies and tv series. The project is organized into several components, each with a specific role in data preparation, analysis, and gameplay.

- Project Structure
py_project.py: This file performs descriptive analysis on the dataset. It generates insights and statistics that help understand the dataset’s structure and content, providing valuable context for both the quiz content and game design.

dataset_merge.py: This file contains Python code that merges and creates two separate datasets. One dataset is used for the descriptive analysis in py_project.py, while the other is specifically tailored for the quiz game itself.

game.py: This is the main game execution file. Running this file launches the quiz game interface, where users can play and answer questions.

quiz.py: This file holds the core algorithm and logic for the quiz game. It includes essential functions like question selection, scoring, and answer validation, forming the backbone of the quiz experience.

- How to Run the Project
Run dataset_merge.py to generate the necessary datasets.
Use py_project.py for initial data analysis (optional but recommended to understand dataset insights).
Execute game.py to start and play the quiz.
