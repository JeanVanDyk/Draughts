from constants import WIDTH, HEIGHT

# Pop Up to congrats the winner
POPUP_WIDTH = WIDTH // 1.1
POPUP_HEIGHT = HEIGHT // 3
POPUP_X = WIDTH // 2 - POPUP_WIDTH // 2
POPUP_Y = 2 * HEIGHT // 5 - POPUP_HEIGHT // 2

# For the choices
CHOICE_WIDTH = POPUP_WIDTH // 4
CHOICE_HEIGHT = POPUP_HEIGHT // 2

WHITE_X = POPUP_X + CHOICE_WIDTH // 4
WHITE_Y = POPUP_Y + CHOICE_HEIGHT // 2

BLACK_X = POPUP_X + 6 * CHOICE_WIDTH // 4
BLACK_Y = POPUP_Y + CHOICE_HEIGHT // 2

RANDOM_X = POPUP_X + 11 * CHOICE_WIDTH // 4
RANDOM_Y = POPUP_Y + CHOICE_HEIGHT // 2
