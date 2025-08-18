from typing import Dict, Optional
import turtle as t
import os

class LSystem:
    def __init__(
        self,
        *,
        axiom: str,
        degrees: float,
        generations: int,
        len_factor: Optional[float] = None,
        rules: Dict[str, str],
        **kwargs

    ) -> None:
        self.axiom = axiom
        self.degrees = degrees
        self.generations = generations
        self.rules = rules
        self.len_factor = len_factor or 0.0

        self.__system = self.__build_system()
        self.__line_len = 10

    def __build_system(self) -> str:
        initial_string = self.axiom
        next_string = ""
        for _ in range(self.generations):
            for char in initial_string:
                next_string += self.rules.get(char) or char
            initial_string = next_string
            next_string = ""
        return initial_string

    def render(self) -> None:
        t.hideturtle()
        t.speed(0) # Highest speed animation
        t.tracer(0, 0) # No animations
        t.left(90) # Face starting up

        stack = []

        for char in self.__system:
            match char:
                case 'F':
                    t.forward(self.__line_len)
                case '+':
                    t.left(self.degrees)
                case '-':
                    t.right(self.degrees)
                case '[':
                    state = (t.pos(), t.heading())
                    stack.append(state)
                case ']':
                    (x, y), heading = stack.pop()
                    t.teleport(x, y)
                    t.setheading(heading)
                case '>':
                    self.__line_len *= self.len_factor;
                case '<':
                    self.__line_len /= self.len_factor;
                case '|':
                    t.left(180)
                case _: continue
        t.update()

GENERATIONS = 4
RULESETS = [
  {
    "name": "Square Wave",
    "rules": {
      "X": "+YF-XFX-FY+",
      "Y": "-XF+YFY+FX-",
    },
    "axiom": "X",
    "degrees": 90,
  },
  {
    "name": "Branch",
    "rules": {
      "F": "FF",
      "X": "F-[[X]+X]+F[+FX]-X",
    },
    "axiom": "X",
    "degrees": 22.5,
  },
  {
    "name": "Bush",
    "rules": {
      "F": "FF+[+F-F-F]-[-F+F+F]",
    },
    "axiom": "F",
    "degrees": 22.5,
  },
  {
    "name": "Stick",
    "rules": {
      "F": "FF",
      "X": "F[+X]F[-X]+X",
    },
    "axiom": "X",
    "degrees": 20,
  },
  {
    "name": "Triangle",
    "rules": {
      "F": "F-F+F",
    },
    "axiom": "F+F+F",
    "degrees": 120,
  },
  {
    "name": "Pentaplexity",
    "rules": {
      "F": "F++F++F|F-F++F",
    },
    "axiom": " F++F++F++F++F",
    "degrees": 36,
  },
]

def print_choices():
    os.system('clear')
    rule_names = map(lambda x: x['name'], RULESETS)
    print("The following rulesets are available:")
    for i, rule in enumerate(rule_names, 1):
        print(f"  {i}. {rule}")

def run_loop():
    global GENERATIONS
    try:
        print_choices()
        choice = input(">> ").strip()
        if choice.startswith("gen"):
            num = choice.removeprefix("gen").strip()
            GENERATIONS = int(num)
        elif choice in ('quit', 'exit', 'q'):
            return True
        else:
            t.reset()
            index = int(choice) - 1
            rule = RULESETS[index]
            system = LSystem(**rule, generations=GENERATIONS)
            system.render()
    except ValueError:
        print("Invalid number, please enter a valid number.")
    except KeyboardInterrupt:
        print("Goodbye.")
        return True

def main():
    done = False
    while not done:
        done = run_loop()
    t.bye()

if __name__ == "__main__":
    main()
