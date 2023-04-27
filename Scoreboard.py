import csv


class ScoreBoard:
    pass
def create():
    scoreboard = ScoreBoard()
    scoreboard.player_names = []
    scoreboard.scores = []
    return scoreboard

def create_from_csv(csv_filename, score_column_number):
    scoreboard = create()
    with open(csv_filename, encoding='latin-1', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            scoreboard.player_names.append(row[0])
            scoreboard.scores.append(int(row[score_column_number]))

    return scoreboard

def get_player_names(scoreboard):
    return scoreboard.player_names

def get_scores(scoreboard):
    return scoreboard.scores

def add_score( playername, score):
    found = False
    rows = []
    with open("./test.csv", mode='r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row and row[0] == playername:
                row[1] = score
                found = True
            rows.append(row)

    if not found:
        rows.append([playername, score])

    with open("./test.csv", mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for row in rows:
            writer.writerow(row)

def get_top_scores(scoreboard):
    sorted_scores = sorted(scoreboard.scores, reverse=True)
    top_scores = sorted_scores[:10]
    top_player_names = [scoreboard.player_names[scoreboard.scores.index(score)] for score in top_scores]
    top_player_scores = top_scores
    return list(zip(top_player_names, top_player_scores))




if __name__ == "__main__":
    scoreboard = create_from_csv("./test.csv", 1)
    add_score("Foxtrot",9999)
    add_score("Luc",5000)
    add_score("Foxtro",9000)
    add_score("Foxtrt",8000)
    add_score("Foxtr",7000)
    add_score("Foxt",6000)
    add_score("Fox",4000)
    add_score("Fo",3000)
    add_score("F",2000)
    add_score("FoxtrotNice",500)
    add_score("Besson",200)
    add_score("Patate",3000)
    print(get_top_scores(scoreboard))
