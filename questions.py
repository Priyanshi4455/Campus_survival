"""CAMPUS_SURVIVE Module 2: Questions and Decision System.

No GUI imports and no file persistence. The caller (game engine/login module)
owns saving the shared player dictionary.
"""

import hashlib
import random
from copy import deepcopy

STAT_KEYS = ("happiness", "attendance", "grades", "energy", "stress", "money")
CLAMPED_STATS = ("happiness", "attendance", "grades", "energy", "stress")
TOTAL_DAYS = 15

QUESTIONS = [
    {
        "id": "D1Q1",
        "day": 1,
        "title": "Assignment Deadline",
        "scenario": "Your assignment is due tonight, and you have only the evening left to complete it. You also promised to join your friends for a celebration.",
        "choices": [
            {
                "text": "Complete the assignment independently and submit it on time",
                "effects": {
                    "happiness": 0,
                    "attendance": 0,
                    "grades": 10,
                    "energy": -10,
                    "stress": -5,
                    "money": 0
                },
                "feedback": "You submitted the assignment on time, but gave up most of your evening to finish it."
            },
            {
                "text": "Join the celebration and accept that the assignment may be late",
                "effects": {
                    "happiness": 10,
                    "attendance": 0,
                    "grades": -10,
                    "energy": 5,
                    "stress": 5,
                    "money": -300
                },
                "feedback": "You enjoyed the celebration, but leaving the assignment unfinished affected your grades and increased your stress."
            },
            {
                "text": "Ask a classmate for guidance, then finish the work yourself",
                "effects": {
                    "happiness": 5,
                    "attendance": 0,
                    "grades": 5,
                    "energy": -5,
                    "stress": -5,
                    "money": 0
                },
                "feedback": "A classmate's guidance helped you submit your own work and reduced some of the pressure."
            }
        ]
    },
    {
        "id": "D2Q1",
        "day": 2,
        "title": "An Early Lecture After a Late Study Session",
        "scenario": "You studied late and did not get enough sleep. An important lecture starts soon, and you need to decide how to balance attendance with rest.",
        "choices": [
            {
                "text": "Attend the lecture and review the notes later",
                "effects": {
                    "happiness": -2,
                    "attendance": 10,
                    "grades": 3,
                    "energy": -10,
                    "stress": -2,
                    "money": 0
                },
                "feedback": "You received the lecture notes and stayed on track, although the lack of sleep affected your energy."
            },
            {
                "text": "Get another hour of sleep and ask a classmate for notes",
                "effects": {
                    "happiness": 5,
                    "attendance": -10,
                    "grades": -3,
                    "energy": 10,
                    "stress": -5,
                    "money": 0
                },
                "feedback": "The extra sleep restored some energy, but you missed the lecture and lost attendance credit."
            },
            {
                "text": "Attend the lecture, then take a short nap between classes",
                "effects": {
                    "happiness": 2,
                    "attendance": 5,
                    "grades": 2,
                    "energy": -5,
                    "stress": -3,
                    "money": 0
                },
                "feedback": "You attended the lecture and made time to rest afterward, balancing both priorities."
            }
        ]
    },
    {
        "id": "D3Q1",
        "day": 3,
        "title": "An Unexpected Class Test",
        "scenario": "Your instructor announces a short test without warning. You have revised some topics, but others still need attention.",
        "choices": [
            {
                "text": "Answer the questions you know and manage your time carefully",
                "effects": {
                    "happiness": -2,
                    "attendance": 0,
                    "grades": 5,
                    "energy": -5,
                    "stress": 3,
                    "money": 0
                },
                "feedback": "You made the best use of your preparation and identified topics to review before the next test."
            },
            {
                "text": "Use the remaining time to review a classmate's summary notes",
                "effects": {
                    "happiness": 0,
                    "attendance": 0,
                    "grades": 7,
                    "energy": -8,
                    "stress": -2,
                    "money": 0
                },
                "feedback": "A quick review helped you recall some material, although you had little time to pause and prepare."
            },
            {
                "text": "Rush through the test without reviewing or planning your time",
                "effects": {
                    "happiness": -5,
                    "attendance": 0,
                    "grades": -5,
                    "energy": -3,
                    "stress": 10,
                    "money": 0
                },
                "feedback": "Rushing made it harder to focus. A brief pause and a quick review could help you approach the next test more calmly."
            }
        ]
    },
    {
        "id": "D4Q1",
        "day": 4,
        "title": "A Social Invitation Before an Early Lecture",
        "scenario": "Your friends are planning an evening out. You have an early lecture tomorrow and a limited weekly budget.",
        "choices": [
            {
                "text": "Join them, set a spending limit, and leave at a reasonable time",
                "effects": {
                    "happiness": 10,
                    "attendance": 0,
                    "grades": 0,
                    "energy": -5,
                    "stress": -5,
                    "money": -250
                },
                "feedback": "You enjoyed time with your friends and kept your spending within the limit you set."
            },
            {
                "text": "Decline the invitation and use the evening to study",
                "effects": {
                    "happiness": -3,
                    "attendance": 0,
                    "grades": 5,
                    "energy": -5,
                    "stress": 2,
                    "money": 0
                },
                "feedback": "You completed your study goal, but missed an opportunity to spend time with your friends."
            },
            {
                "text": "Suggest a lower-cost plan that ends early",
                "effects": {
                    "happiness": 7,
                    "attendance": 0,
                    "grades": 1,
                    "energy": -2,
                    "stress": -4,
                    "money": -80
                },
                "feedback": "The lower-cost plan let you stay connected while protecting your budget and sleep."
            }
        ]
    },
    {
        "id": "D5Q1",
        "day": 5,
        "title": "Limited Pocket Money",
        "scenario": "You have limited money for the week and need to cover course materials, meals, and transport. A friend has invited you to an expensive cafe.",
        "choices": [
            {
                "text": "Plan your essential expenses before making any optional purchases",
                "effects": {
                    "happiness": 0,
                    "attendance": 0,
                    "grades": 2,
                    "energy": 0,
                    "stress": -4,
                    "money": 0
                },
                "feedback": "A clear budget helped you reserve money for essential expenses throughout the week."
            },
            {
                "text": "Spend now at your favourite cafe and adjust your budget later",
                "effects": {
                    "happiness": 8,
                    "attendance": 0,
                    "grades": 0,
                    "energy": 2,
                    "stress": -2,
                    "money": -350
                },
                "feedback": "The treat improved your mood, but left less money for essentials later in the week."
            },
            {
                "text": "Bring lunch from home and use digital course materials where possible",
                "effects": {
                    "happiness": -1,
                    "attendance": 0,
                    "grades": 2,
                    "energy": 0,
                    "stress": -2,
                    "money": 100
                },
                "feedback": "These practical changes reduced your costs while keeping your course materials accessible."
            }
        ]
    },
    {
        "id": "D6Q1",
        "day": 6,
        "title": "Group Project Conflict",
        "scenario": "A teammate has missed several tasks, and your group-project deadline is approaching. The group has not yet agreed on how to address the problem.",
        "choices": [
            {
                "text": "Speak with the teammate calmly and agree on clear responsibilities",
                "effects": {
                    "happiness": 2,
                    "attendance": 0,
                    "grades": 7,
                    "energy": -4,
                    "stress": -4,
                    "money": 0
                },
                "feedback": "Clear responsibilities improved coordination and helped the project move forward."
            },
            {
                "text": "Complete the missing work yourself to protect the deadline",
                "effects": {
                    "happiness": -3,
                    "attendance": 0,
                    "grades": 5,
                    "energy": -15,
                    "stress": 8,
                    "money": 0
                },
                "feedback": "The project stayed on schedule, but taking on the extra work left you exhausted."
            },
            {
                "text": "Ask the instructor to help the group resolve the issue",
                "effects": {
                    "happiness": -1,
                    "attendance": 0,
                    "grades": 4,
                    "energy": -2,
                    "stress": -3,
                    "money": 0
                },
                "feedback": "The instructor helped clarify expectations, although arranging a discussion took time."
            },
            {
                "text": "Confront the teammate angrily in the group chat",
                "effects": {
                    "happiness": -5,
                    "attendance": 0,
                    "grades": -2,
                    "energy": -4,
                    "stress": 8,
                    "money": 0
                },
                "feedback": "The confrontation expressed your frustration, but increased tension and made coordination harder."
            }
        ]
    },
    {
        "id": "D7Q1",
        "day": 7,
        "title": "Exam Preparation",
        "scenario": "Your exam is one week away, and the syllabus is extensive. You also have other coursework to complete, so you need a realistic study plan.",
        "choices": [
            {
                "text": "Prioritize difficult and high-value topics, then schedule focused study blocks",
                "effects": {
                    "happiness": -1,
                    "attendance": 0,
                    "grades": 8,
                    "energy": -8,
                    "stress": -3,
                    "money": 0
                },
                "feedback": "Prioritizing helped you cover important topics and made the remaining work easier to plan."
            },
            {
                "text": "Study all day without breaks to cover as much material as possible",
                "effects": {
                    "happiness": -5,
                    "attendance": 0,
                    "grades": 6,
                    "energy": -18,
                    "stress": 8,
                    "money": 0
                },
                "feedback": "You covered a lot of material, but studying without breaks reduced your energy and focus."
            },
            {
                "text": "Join a study group to discuss difficult topics",
                "effects": {
                    "happiness": 4,
                    "attendance": 0,
                    "grades": 5,
                    "energy": -5,
                    "stress": -4,
                    "money": -50
                },
                "feedback": "Discussing difficult concepts with classmates clarified some questions, although the session cost you time and money."
            }
        ]
    },
    {
        "id": "D8Q1",
        "day": 8,
        "title": "Managing Workload and Well-Being",
        "scenario": "After a full day of classes and assignments, your energy is low and your stress is high. You still have work due tomorrow.",
        "choices": [
            {
                "text": "Take a short break, drink water, and have a proper meal before continuing",
                "effects": {
                    "happiness": 4,
                    "attendance": 0,
                    "grades": 0,
                    "energy": 15,
                    "stress": -10,
                    "money": -100
                },
                "feedback": "Taking a break and eating helped restore your energy and made the workload feel more manageable."
            },
            {
                "text": "Have coffee and continue working without changing your schedule",
                "effects": {
                    "happiness": 0,
                    "attendance": 0,
                    "grades": 3,
                    "energy": 5,
                    "stress": 5,
                    "money": -80
                },
                "feedback": "You made progress, but continued working while tired and added to your stress."
            },
            {
                "text": "Reprioritize the tasks, complete the most urgent one, and go to bed early",
                "effects": {
                    "happiness": 3,
                    "attendance": 0,
                    "grades": -1,
                    "energy": 20,
                    "stress": -8,
                    "money": 0
                },
                "feedback": "Rest helped you recover, while reprioritizing kept the most urgent task on track."
            }
        ]
    },
    {
        "id": "D9Q1",
        "day": 9,
        "title": "Unexpected Expenses",
        "scenario": "Unexpected transport and project-material costs have reduced your semester budget. You need to cover the required expenses without creating a larger financial problem.",
        "choices": [
            {
                "text": "Review your expenses and pause non-essential spending",
                "effects": {
                    "happiness": -1,
                    "attendance": 0,
                    "grades": 1,
                    "energy": 0,
                    "stress": -3,
                    "money": 0
                },
                "feedback": "Tracking your expenses gave you a clearer plan for protecting your remaining budget."
            },
            {
                "text": "Use some savings to pay for the required materials and transport",
                "effects": {
                    "happiness": 1,
                    "attendance": 0,
                    "grades": 2,
                    "energy": 0,
                    "stress": -4,
                    "money": -500
                },
                "feedback": "You covered the immediate costs, but reduced the savings available for later in the semester."
            },
            {
                "text": "Ask a trusted friend for a small loan and agree on a repayment date",
                "effects": {
                    "happiness": -1,
                    "attendance": 0,
                    "grades": 2,
                    "energy": 0,
                    "stress": 2,
                    "money": 0
                },
                "feedback": "The loan covered the immediate expense, but you will need to follow the repayment plan."
            }
        ]
    },
    {
        "id": "D10Q1",
        "day": 10,
        "title": "An Internship Application Deadline",
        "scenario": "An internship application closes tonight, and you still have an assignment due tomorrow. You have enough time to make progress on both, but not to perfect both.",
        "choices": [
            {
                "text": "Submit your current resume and application immediately, then finish the assignment",
                "effects": {
                    "happiness": 1,
                    "attendance": 0,
                    "grades": 2,
                    "energy": -7,
                    "stress": 3,
                    "money": 0
                },
                "feedback": "You met the internship deadline and protected time for your assignment, but a rushed application may not present your strengths clearly."
            },
            {
                "text": "Prioritize the assignment and accept that you may miss this application deadline",
                "effects": {
                    "happiness": 0,
                    "attendance": 0,
                    "grades": 5,
                    "energy": -4,
                    "stress": 1,
                    "money": 0
                },
                "feedback": "You protected your academic deadline, but gave up this internship opportunity."
            },
            {
                "text": "Check the application requirements, tailor your resume, and reserve a focused block for the assignment",
                "effects": {
                    "happiness": 4,
                    "attendance": 0,
                    "grades": 3,
                    "energy": -8,
                    "stress": -4,
                    "money": 0
                },
                "feedback": "You checked the requirements and divided your time deliberately, giving both the application and assignment focused attention."
            }
        ]
    },
    {
        "id": "D11Q1",
        "day": 11,
        "title": "A Lecture or Time with Friends",
        "scenario": "The lecture topic does not interest you, and your friends are heading off campus. Attendance matters in this course, but you also need a break.",
        "choices": [
            {
                "text": "Attend the lecture and take notes, even if the topic is not engaging",
                "effects": {
                    "happiness": -1,
                    "attendance": 8,
                    "grades": 3,
                    "energy": -4,
                    "stress": -1,
                    "money": 0
                },
                "feedback": "You maintained your attendance and captured the key material, although the lecture was not especially engaging."
            },
            {
                "text": "Skip the lecture and spend the time with your friends",
                "effects": {
                    "happiness": 7,
                    "attendance": -10,
                    "grades": -3,
                    "energy": 3,
                    "stress": -2,
                    "money": -150
                },
                "feedback": "You got a break with your friends, but missed course content and attendance credit."
            },
            {
                "text": "Attend the lecture, then meet your friends afterward",
                "effects": {
                    "happiness": 4,
                    "attendance": 5,
                    "grades": 2,
                    "energy": -3,
                    "stress": -2,
                    "money": -50
                },
                "feedback": "You attended the lecture and still made time to see your friends, though the day felt busier."
            }
        ]
    },
    {
        "id": "D12Q1",
        "day": 12,
        "title": "Internal Assessment",
        "scenario": "An upcoming assessment will contribute to your final grade. One topic is challenging, and you also need to verify that your coursework submission is complete.",
        "choices": [
            {
                "text": "Practice the difficult topic, then check your submission before the assessment",
                "effects": {
                    "happiness": -1,
                    "attendance": 0,
                    "grades": 9,
                    "energy": -8,
                    "stress": -3,
                    "money": 0
                },
                "feedback": "Focused practice strengthened your understanding, and checking the submission helped you avoid an administrative mistake."
            },
            {
                "text": "Review familiar topics first to secure the marks you already understand",
                "effects": {
                    "happiness": 1,
                    "attendance": 0,
                    "grades": 3,
                    "energy": -4,
                    "stress": -2,
                    "money": 0
                },
                "feedback": "You reinforced familiar material, but the more challenging topic still needs attention."
            },
            {
                "text": "Complete a timed practice assessment with a classmate",
                "effects": {
                    "happiness": 3,
                    "attendance": 0,
                    "grades": 6,
                    "energy": -6,
                    "stress": -4,
                    "money": -30
                },
                "feedback": "The practice assessment revealed timing issues and knowledge gaps, though reviewing it took extra time."
            }
        ]
    },
    {
        "id": "D13Q1",
        "day": 13,
        "title": "An Internship Fair During Exam Preparation",
        "scenario": "A campus internship fair is taking place today, and several employers match your career interests. Your exam is approaching, and you still have revision to complete.",
        "choices": [
            {
                "text": "Attend the most relevant employer sessions, then follow your planned study schedule",
                "effects": {
                    "happiness": 7,
                    "attendance": 0,
                    "grades": 3,
                    "energy": -5,
                    "stress": -3,
                    "money": -200
                },
                "feedback": "You explored relevant internship opportunities and completed a study session, although balancing both required careful time management."
            },
            {
                "text": "Spend the day networking at the fair and reschedule your revision",
                "effects": {
                    "happiness": 12,
                    "attendance": 0,
                    "grades": -4,
                    "energy": -8,
                    "stress": -3,
                    "money": -500
                },
                "feedback": "You made useful professional connections, but will need to reorganize your remaining revision before the exam."
            },
            {
                "text": "Skip the fair and use the day to study in the library",
                "effects": {
                    "happiness": -4,
                    "attendance": 0,
                    "grades": 7,
                    "energy": -7,
                    "stress": 2,
                    "money": 0
                },
                "feedback": "You made substantial progress on revision, but missed a chance to learn about internship opportunities."
            }
        ]
    },
    {
        "id": "D14Q1",
        "day": 14,
        "title": "Final Exam Preparation",
        "scenario": "Your final exam is tomorrow. You have reviewed most chapters, but need to decide how to use your remaining time without sacrificing the rest you need to focus.",
        "choices": [
            {
                "text": "Review your key notes, prepare what you need for the exam, and go to bed on time",
                "effects": {
                    "happiness": 1,
                    "attendance": 0,
                    "grades": 7,
                    "energy": 10,
                    "stress": -6,
                    "money": 0
                },
                "feedback": "You reinforced key material and protected time for rest, supporting a balanced exam plan."
            },
            {
                "text": "Stay up all night to cover every remaining topic",
                "effects": {
                    "happiness": -4,
                    "attendance": 0,
                    "grades": 5,
                    "energy": -20,
                    "stress": 10,
                    "money": -100
                },
                "feedback": "You reviewed more topics, but losing sleep may make it harder to concentrate during the exam."
            },
            {
                "text": "Do a focused question-and-answer review with a classmate, then rest",
                "effects": {
                    "happiness": 3,
                    "attendance": 0,
                    "grades": 6,
                    "energy": -8,
                    "stress": -3,
                    "money": -50
                },
                "feedback": "Questioning each other strengthened recall, although you may still need to review topics you could not explain."
            }
        ]
    },
    {
        "id": "D15Q1",
        "day": 15,
        "title": "Reflecting on the Semester",
        "scenario": "The semester has ended. You are reviewing your academic progress, relationships, and well-being while deciding how to prepare for the next term.",
        "choices": [
            {
                "text": "Review your results and set specific, realistic goals for next semester",
                "effects": {
                    "happiness": 2,
                    "attendance": 0,
                    "grades": 3,
                    "energy": -2,
                    "stress": -4,
                    "money": 0
                },
                "feedback": "Reviewing your progress helped you set clear goals for the next semester."
            },
            {
                "text": "Celebrate the end of the semester with your friends",
                "effects": {
                    "happiness": 10,
                    "attendance": 0,
                    "grades": 0,
                    "energy": -3,
                    "stress": -6,
                    "money": -400
                },
                "feedback": "Celebrating helped you recognize the semester's milestones and strengthen your friendships."
            },
            {
                "text": "Take time to rest and focus on your well-being",
                "effects": {
                    "happiness": 6,
                    "attendance": 0,
                    "grades": 0,
                    "energy": 15,
                    "stress": -8,
                    "money": 0
                },
                "feedback": "You gave yourself time to recover and approach the next semester with renewed energy."
            },
            {
                "text": "Create a weekly study routine before the next semester begins",
                "effects": {
                    "happiness": 0,
                    "attendance": 0,
                    "grades": 5,
                    "energy": -3,
                    "stress": -2,
                    "money": 0
                },
                "feedback": "A routine gave you a practical starting point for a more organized semester."
            }
        ]
    }
]


def get_question(day, student_id):
    """Return the question assigned to this student on a valid day, or None."""
    if not isinstance(day, int) or isinstance(day, bool) or not 1 <= day <= TOTAL_DAYS:
        return None
    if not isinstance(student_id, str) or not student_id.strip():
        return None

    order = generate_question_order(student_id)
    question_id = order[day - 1]
    return get_question_by_id(question_id)


def get_question_by_id(question_id):
    """Return a detached copy of a question by its unique ID, or None."""
    for question in QUESTIONS:
        if question["id"] == question_id:
            return deepcopy(question)
    return None


def generate_question_order(student_id):
    """Generate a stable student-specific order of all 15 question IDs.

    The sequence is deterministic for each Student ID. Store the returned list
    in player["question_order"] so the game engine can persist/resume it.
    """
    if not isinstance(student_id, str) or not student_id.strip():
        return []

    seed_text = "CAMPUS_SURVIVE:questions:v1:" + student_id.strip()
    seed = int(hashlib.sha256(seed_text.encode("utf-8")).hexdigest(), 16)
    question_ids = [question["id"] for question in QUESTIONS]
    random.Random(seed).shuffle(question_ids)
    return question_ids


def _get_effects(choice):
    """Return all six effect keys, defaulting missing values to zero."""
    effects = choice.get("effects", {})
    return {key: effects.get(key, 0) for key in STAT_KEYS}


def get_choice_feedback(question, choice_index):
    """Return feedback for the selected choice; invalid indexes raise ValueError."""
    if not isinstance(question, dict) or not isinstance(question.get("choices"), list):
        raise ValueError("question must contain a choices list")

    if not isinstance(choice_index, int) or isinstance(choice_index, bool):
        raise ValueError("choice_index must be an integer")
    choices = question["choices"]
    if choice_index < 0 or choice_index >= len(choices):
        raise ValueError("choice_index is out of range")

    feedback = choices[choice_index].get("feedback")
    if not isinstance(feedback, str):
        raise ValueError("selected choice has no valid feedback")
    return feedback


def apply_choice(player, question, choice_index):
    """Apply choice effects in-place and return (updated_player, feedback).

    Five wellness/academic stats are clamped to 0..100. Money is kept
    non-negative. This function deliberately does not advance current_day.
    Invalid input raises ValueError or TypeError before changing player stats.
    """
    if not isinstance(player, dict):
        raise TypeError("player must be a dictionary")
    if not isinstance(question, dict) or not isinstance(question.get("choices"), list):
        raise ValueError("question must contain a choices list")
    if not isinstance(choice_index, int) or isinstance(choice_index, bool):
        raise ValueError("choice_index must be an integer")

    choices = question["choices"]
    if choice_index < 0 or choice_index >= len(choices):
        raise ValueError("choice_index is out of range")

    choice = choices[choice_index]
    effects = _get_effects(choice)

    # Validate effects before mutating anything, avoiding partial updates.
    for key, effect in effects.items():
        if not isinstance(effect, (int, float)) or isinstance(effect, bool):
            raise ValueError(f"effect for {key!r} must be numeric")
        if key not in player:
            raise ValueError(f"player is missing required stat {key!r}")
        if not isinstance(player[key], (int, float)) or isinstance(player[key], bool):
            raise ValueError(f"player stat {key!r} must be numeric")

    feedback = get_choice_feedback(question, choice_index)

    for key, effect in effects.items():
        new_value = player[key] + effect
        if key in CLAMPED_STATS:
            new_value = max(0, min(100, new_value))
        elif key == "money":
            new_value = max(0, new_value)
        player[key] = new_value

    return player, feedback
