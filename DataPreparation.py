class DataPreparation:
    TEAMS = [
        {"id": 1, "name": "Russia", "points": 0},
        {"id": 2, "name": "Saudi Arabia", "points": 0},
        {"id": 3, "name": "Egypt", "points": 0},
        {"id": 4, "name": "Uruguay", "points": 0},

        {"id": 5, "name": "Portugal", "points": 0},
        {"id": 6, "name": "Spain", "points": 0},
        {"id": 7, "name": "Morocco", "points": 0},
        {"id": 8, "name": "Iran", "points": 0},

        {"id": 9, "name": "France", "points": 0},
        {"id": 10, "name": "Australia", "points": 0},
        {"id": 11, "name": "Peru", "points": 0},
        {"id": 12, "name": "Denmark", "points": 0},

        {"id": 13, "name": "Argentina", "points": 0},
        {"id": 14, "name": "Iceland", "points": 0},
        {"id": 15, "name": "Croatia", "points": 0},
        {"id": 16, "name": "Nigeria", "points": 0},

        {"id": 17, "name": "Brazil", "points": 0},
        {"id": 18, "name": "Switzerland", "points": 0},
        {"id": 19, "name": "Costa Rica", "points": 0},
        {"id": 20, "name": "Serbia", "points": 0},

        {"id": 21, "name": "Germany", "points": 0},
        {"id": 22, "name": "Mexico", "points": 0},
        {"id": 23, "name": "Sweden", "points": 0},
        {"id": 24, "name": "Korea Republic", "points": 0},

        {"id": 25, "name": "Belgium", "points": 0},
        {"id": 26, "name": "Panama", "points": 0},
        {"id": 27, "name": "Tunisia", "points": 0},
        {"id": 28, "name": "England", "points": 0},

        {"id": 29, "name": "Poland", "points": 0},
        {"id": 30, "name": "Senegal", "points": 0},
        {"id": 31, "name": "Colombia", "points": 0},
        {"id": 32, "name": "Japan", "points": 0}
    ]

    GROUPS = [
        {"id": "A", "teams": [1, 2, 3, 4], "first": 1, "second": 2},
        {"id": "B", "teams": [5, 6, 7, 8], "first": 5, "second": 6},
        {"id": "C", "teams": [9, 10, 11, 12], "first": 9, "second": 10},
        {"id": "D", "teams": [13, 14, 15, 16], "first": 13, "second": 14},
        {"id": "E", "teams": [17, 18, 19, 20], "first": 17, "second": 18},
        {"id": "F", "teams": [21, 22, 23, 24], "first": 21, "second": 22},
        {"id": "G", "teams": [25, 26, 27, 28], "first": 25, "second": 26},
        {"id": "H", "teams": [29, 30, 31, 32], "first": 29, "second": 30},
    ]

    # Stages: 1 - group, 2 - eight-finals, 3 - quarter-finals, 4 - semi-final, 5 - 3rd place match, 6 - final
    MATCHES = [
        {"id": 1, "home": 1, "away": 2, "stage": 1},
        {"id": 2, "home": 3, "away": 4, "stage": 1},
        {"id": 3, "home": 7, "away": 8, "stage": 1},
        {"id": 4, "home": 5, "away": 6, "stage": 1},
        {"id": 5, "home": 9, "away": 10, "stage": 1},
        {"id": 6, "home": 13, "away": 14, "stage": 1},
        {"id": 7, "home": 11, "away": 12, "stage": 1},
        {"id": 8, "home": 15, "away": 16, "stage": 1},
        {"id": 9, "home": 19, "away": 20, "stage": 1},
        {"id": 10, "home": 21, "away": 22, "stage": 1},
        {"id": 11, "home": 17, "away": 18, "stage": 1},
        {"id": 12, "home": 23, "away": 24, "stage": 1},
        {"id": 13, "home": 25, "away": 26, "stage": 1},
        {"id": 14, "home": 27, "away": 28, "stage": 1},
        {"id": 15, "home": 31, "away": 32, "stage": 1},
        {"id": 16, "home": 29, "away": 30, "stage": 1},
        {"id": 17, "home": 1, "away": 3, "stage": 1},
        {"id": 18, "home": 5, "away": 7, "stage": 1},
        {"id": 19, "home": 4, "away": 2, "stage": 1},
        {"id": 20, "home": 8, "away": 6, "stage": 1},
        {"id": 21, "home": 12, "away": 10, "stage": 1},
        {"id": 22, "home": 9, "away": 11, "stage": 1},
        {"id": 23, "home": 13, "away": 15, "stage": 1},
        {"id": 24, "home": 17, "away": 19, "stage": 1},
        {"id": 25, "home": 16, "away": 14, "stage": 1},
        {"id": 26, "home": 20, "away": 18, "stage": 1},
        {"id": 27, "home": 25, "away": 27, "stage": 1},
        {"id": 28, "home": 24, "away": 22, "stage": 1},
        {"id": 29, "home": 21, "away": 23, "stage": 1},
        {"id": 30, "home": 28, "away": 26, "stage": 1},
        {"id": 31, "home": 32, "away": 30, "stage": 1},
        {"id": 32, "home": 29, "away": 31, "stage": 1},
        {"id": 33, "home": 4, "away": 1, "stage": 1},
        {"id": 34, "home": 2, "away": 3, "stage": 1},
        {"id": 35, "home": 6, "away": 7, "stage": 1},
        {"id": 36, "home": 8, "away": 5, "stage": 1},
        {"id": 37, "home": 10, "away": 11, "stage": 1},
        {"id": 38, "home": 12, "away": 9, "stage": 1},
        {"id": 39, "home": 16, "away": 13, "stage": 1},
        {"id": 40, "home": 14, "away": 15, "stage": 1},
        {"id": 41, "home": 24, "away": 21, "stage": 1},
        {"id": 42, "home": 22, "away": 23, "stage": 1},
        {"id": 43, "home": 20, "away": 17, "stage": 1},
        {"id": 44, "home": 18, "away": 19, "stage": 1},
        {"id": 45, "home": 32, "away": 29, "stage": 1},
        {"id": 46, "home": 30, "away": 31, "stage": 1},
        {"id": 47, "home": 26, "away": 27, "stage": 1},
        {"id": 48, "home": 25, "away": 28, "stage": 1},
        {"id": 49, "home": "1C", "away": "2D", "stage": 2},
        {"id": 50, "home": "1A", "away": "2B", "stage": 2},
        {"id": 51, "home": "1B", "away": "2A", "stage": 2},
        {"id": 52, "home": "1D", "away": "2C", "stage": 2},
        {"id": 53, "home": "1E", "away": "2F", "stage": 2},
        {"id": 54, "home": "1G", "away": "2H", "stage": 2},
        {"id": 55, "home": "1F", "away": "2E", "stage": 2},
        {"id": 56, "home": "1H", "away": "2G", "stage": 2},
        {"id": 57, "home": 49, "away": 50, "stage": 3},
        {"id": 58, "home": 53, "away": 54, "stage": 3},
        {"id": 59, "home": 55, "away": 56, "stage": 3},
        {"id": 60, "home": 51, "away": 52, "stage": 3},
        {"id": 61, "home": 57, "away": 58, "stage": 4},
        {"id": 62, "home": 59, "away": 60, "stage": 4},
        {"id": 63, "home": 61, "away": 62, "stage": 5},
        {"id": 64, "home": 61, "away": 62, "stage": 6}
    ]

    def __init__(self):
        pass
