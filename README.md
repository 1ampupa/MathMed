# MathMed

## Introduction
This is a desktop game built on Python to improve your mental calculation speed through timed challenge.

## Feature
Currently in early development. Some core mechanics are under implementation.
- Randomised question generator (+, −, ×, ÷) based on difficulty
- Division questions always produce whole numbers
- Basic Local User profile and session system
- Streak system with adaptive difficulty scaling
- Performance summary after each game
- Telemetry data, such as accuracy %, time per question, etc.
- Telemetry data report

## Roadmap
* Proposed
- Fully customisable difficulty levels
- GUI Framework using CustomTkinter for a better experience

* Future plans
- Game modes for different and engaging gameplay, such as Timed Challenge, or Endless questions
- User Save/Load system

## Installation
In order to create a copy of this repository, you need
- a computer
- Python 3.10 or later
- A Python IDE

1. Clone this repository
2. Create a venv (Virtual Environment) (Commands are available below)
3. Run the following commands in your terminal from the project directory:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Project Structure
```
module/
|- core
    |- difficulty_manager.py    Handle Difficulty optimistiser algorithm
    |- operator.py              Store Arithmetic operators enums
    |- quiz_modifier.py         Configuration for the pattern of the quiz
    |- quiz_validator.py        Handle validation of the quiz before sending it to user
    |- quiz.py                  Handle Quiz object
    |- session.py               Handle Game session
    |- user_answer.py           Receive, check user answer
    |- user_telemetry.py        Handle user telemetry data for save/load system
    |- user.py                  Handle User
main.py     # Entry point
```

## Disclaimer
This project is developed in my spare time. Updates may be gradual as I have other commitments and this is only a personal project, I hope you understand :D

Thank you and good luck coding!

@1ampupa 05 Mar 2026