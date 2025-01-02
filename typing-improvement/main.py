import curses
import time

def typing_trainer_curses(stdscr):
    stdscr.clear()
    stdscr.scrollok(True)

    # Example sentence
    sentence = "I’m working on a longer sentence with diverse punctuation and around 80-100 characters, potentially integrating multiple lines, to enrich practice."
    stdscr.addstr(f"Type the following sentence and press Enter:\n{sentence}\n\n")
    stdscr.addstr("Start typing:\n")
    stdscr.refresh()

    key_times = []
    transitions = []
    typed_chars = []

    prev_time = time.time()
    prev_char = None

    while True:
        c = stdscr.getch()
        current_time = time.time()

        # If user presses Enter, exit
        if c == 10:  # Enter
            break

        # Backspace handling
        if c in (curses.KEY_BACKSPACE, 127, 8):
            if typed_chars:
                typed_chars.pop()
                if key_times:
                    key_times.pop()
                if transitions:
                    transitions.pop()

                # Remove last character on screen
                y, x = stdscr.getyx()
                if x > 0:
                    stdscr.move(y, x - 1)
                    stdscr.delch()
            continue

        # If we've already typed the entire sentence, ignore other inputs
        if len(typed_chars) >= len(sentence):
            continue

        # Normal character input
        char = chr(c)
        stdscr.addch(c)
        stdscr.refresh()

        typed_chars.append(char)
        key_times.append(current_time - prev_time)

        # Build transition label (e.g., "a -> b")
        if prev_char is not None:
            transitions.append(f"{prev_char} -> {char}")

        prev_time = current_time
        prev_char = char

    # --------------------
    #       Statistics
    # --------------------
    total_time = sum(key_times)
    avg_time = total_time / len(key_times) if key_times else 0
    min_time = min(key_times) if key_times else 0
    max_time = max(key_times) if key_times else 0

    user_input = "".join(typed_chars)
    truncated_input = user_input[:len(sentence)]
    correct_chars = sum(1 for a, b in zip(truncated_input, sentence) if a == b)
    accuracy = (correct_chars / len(sentence)) * 100 if sentence else 0

    stdscr.addstr("\n\n")
    stdscr.refresh()

    # --------------------
    #       Results
    # --------------------
    stdscr.addstr("\n=== Results ===\n")
    stdscr.addstr(f"Typed text: {truncated_input}\n")
    stdscr.addstr(f"Accuracy: {accuracy:.2f}%\n")
    stdscr.addstr(f"Total time: {total_time:.2f} seconds\n")
    stdscr.addstr(f"Average time per key: {avg_time:.2f} seconds\n")
    stdscr.addstr(f"Fastest key time: {min_time:.2f} seconds\n")
    stdscr.addstr(f"Slowest key time: {max_time:.2f} seconds\n")

    # --------------------
    #    Grouped Transitions
    # --------------------
    # transitions[i] pairs with key_times[i+1] because:
    #  - key_times[0]: time from start to first key
    #  - key_times[i+1]: time for the (i+1)-th typed char
    transition_dict = {}
    for i, transition in enumerate(transitions):
        diff = key_times[i + 1] if (i + 1) < len(key_times) else 0.0
        transition_dict.setdefault(transition, []).append(diff)

    stdscr.addstr("\nTransitions:\n")
    stdscr.addstr(f"Number of transitions: {len(transitions)}\n")

    max_y, max_x = stdscr.getmaxyx()
    for transition, times in transition_dict.items():
        avg_diff = sum(times) / len(times) if times else 0.0
        line = f"{transition}: average {avg_diff:.2f} seconds (count: {len(times)})"

        # Split lines if they exceed the terminal width
        if len(line) >= max_x:
            while len(line) > max_x:
                stdscr.addstr(line[:max_x] + "\n")
                line = line[max_x:]
        stdscr.addstr(line + "\n")

    stdscr.refresh()
    stdscr.getch()

def main():
    curses.wrapper(typing_trainer_curses)

if __name__ == "__main__":
    main()

"""y ->  : average 0.20 seconds (count: 1)
  -> i: average 0.28 seconds (count: 1)
g -> g: average 0.89 seconds (count: 1)
g -> r: average 0.19 seconds (count: 1)
  -> m: average 0.25 seconds (count: 1)
m -> u: average 0.23 seconds (count: 1)
u -> l: average 0.19 seconds (count: 1)
l -> t: average 0.19 seconds (count: 1)
i -> p: average 0.47 seconds (count: 1)
p -> l: average 0.19 seconds (count: 1)
l -> e: average 0.09 seconds (count: 1)
m -> l: average 0.65 seconds (count: 1)
l -> i: average 0.16 seconds (count: 1)
n -> e: average 0.10 seconds (count: 1)
e -> s: average 0.23 seconds (count: 1)
  -> t: average 0.41 seconds (count: 1)
t -> o: average 0.06 seconds (count: 1)
o ->  : average 0.20 seconds (count: 1)
  -> e: average 0.23 seconds (count: 1)
n -> r: average 0.32 seconds (count: 1)
r -> i: average 0.11 seconds (count: 1)
i -> c: average 0.17 seconds (count: 1)
r -> r: average 0.47 seconds (count: 1)
e -> .: average 0.19 seconds (count: 1)

    """