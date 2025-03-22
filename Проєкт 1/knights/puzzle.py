from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Базові припущення: кожен персонаж або лицар, або шахрай, але не обидва одночасно
base_rules = And(
    Or(AKnight, AKnave), Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave), Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave), Not(And(CKnight, CKnave))
)

# Puzzle 0
# A каже: "Я і лицар, і шахрай."
knowledge0 = And(
    base_rules,
    Implication(AKnight, And(AKnight, AKnave)),  # Якщо A лицар, то його твердження істинне (але це суперечність)
    Implication(AKnave, Not(And(AKnight, AKnave)))  # Якщо A шахрай, то він бреше (що узгоджується з неможливістю бути і тим, і іншим)
)

# Puzzle 1
# A каже: "Ми обидва шахраї."
# B нічого не каже.
knowledge1 = And(
    base_rules,
    Implication(AKnight, And(AKnave, BKnave)),  # Якщо A лицар, то він каже правду (але це суперечність)
    Implication(AKnave, Not(And(AKnave, BKnave)))  # Якщо A шахрай, то його твердження хибне
)

# Puzzle 2
# A каже: "Ми однакові."
# B каже: "Ми різні."
knowledge2 = And(
    base_rules,
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    Implication(BKnight, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave)))
)

# Puzzle 3
# A каже: "Я лицар." або "Я шахрай." (але невідомо, яке саме твердження)
# B каже: "A сказав 'Я шахрай'."
# B каже: "C - шахрай."
# C каже: "A - лицар."
knowledge3 = And(
    base_rules,
    Or(Implication(AKnight, AKnight), Implication(AKnight, AKnave)),
    Implication(BKnight, AKnave),  # Якщо B лицар, то A справді шахрай
    Implication(BKnave, Not(AKnave)),  # Якщо B шахрай, то A не шахрай (тобто лицар)
    Implication(BKnight, CKnave),  # Якщо B лицар, то C шахрай
    Implication(BKnave, Not(CKnave)),  # Якщо B шахрай, то C лицар
    Implication(CKnight, AKnight),  # Якщо C лицар, то A лицар
    Implication(CKnave, Not(AKnight))  # Якщо C шахрай, то A не лицар
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")

if __name__ == "__main__":
    main()
