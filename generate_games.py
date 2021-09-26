import csv
import numpy as np
import collections
import random

K_LAPLACE = 1

def probability_func(score_1, score_2):
  delta = abs(score_1 - score_2)
  # 1.1^delta
  # delta**2
  laplace = K_LAPLACE / (delta**2 + float(K_LAPLACE))
  return laplace

def weighted_random_choice(choices):
    max = sum(choices.values())
    pick = random.uniform(0, max)
    current = 0
    for key, value in choices.items():
        current += value
        if current > pick:
            return key

def build_match(snake_map):
  snake = random.choice(list(snake_map.keys()))
  snake_score = snake_map[snake]
  snake_map.pop(snake)
  snake_probabilities = []
  match = [(snake, snake_score)]
  scores = list(snake_map.items())
  random.shuffle(scores)
  for (snake, score) in scores:
    p = probability_func(snake_score, score)
    snake_probabilities.append((snake, p))
  for _ in range(0, 3):
    snake_probabilities = dict(snake_probabilities)
    opponent_id = weighted_random_choice(snake_probabilities)
    match.append((opponent_id, snake_map[opponent_id])) 
    snake_map.pop(opponent_id)
    snake_probabilities.pop(opponent_id)
  return match

def build_matches(snake_map):
  snake_map = dict(snake_map)
  while len(snake_map) % 4 != 0:
    snake_map.pop(random.choice(list(snake_map.keys())))
  
  matches = []
  while snake_map:
    matches.append(build_match(snake_map))
  return matches

def main():
  global K_LAPLACE
  r = csv.DictReader(open('out.csv', 'r'))
  #snake_map = {"good": 1000.0, "good-ish": 900.0, "good-less": 850.0, "good-nice": 800.0, "intermediate": 700.0, "medium": 500.0, "less-medium": 300.0, "less-potato": 200.0, "bad1": 0.0, "bad2":0.0, "bad3":0.0, "bad4": 0.0}
  snake_map = {x["name"]: float(x["score"]) for x in r}
  average_score = sum(snake_map.values()) / len(snake_map)
  K_LAPLACE = average_score**2
  seen_opponents = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))
  seen_scores = collections.defaultdict(list)

  for snake, score in snake_map.items():
    for snake_2, score_2 in snake_map.items():
      print(snake, score, snake_2, score_2, probability_func(score, score_2))
  count_of_games_where_score_difference_is_big = 0
  count_of_games_where_score_difference_is_big_2 = 0
  count_of_games_where_score_difference_is_big_3 = 0
  n_matches = 0
  for i in range(0, 1000):
    result = build_matches(snake_map)
    for match in result:
      scores = [x[1] for x in match]
      smallest = min(scores)
      biggest = max(scores)
      if biggest - smallest > 100:
        count_of_games_where_score_difference_is_big += 1
      if biggest - smallest > 25:
        count_of_games_where_score_difference_is_big_2 += 1
      if biggest - smallest > 250:
        count_of_games_where_score_difference_is_big_3 += 1
      n_matches += 1
      for snake_id, score in match:
        for snake_id_new, score_new in match:
          if snake_id_new != snake_id:
            seen_opponents[snake_id][snake_id_new] += 1
            seen_scores[snake_id].append(score_new)

  print("delta exceeds 25 in  " + str(count_of_games_where_score_difference_is_big_2 / n_matches))
  print("delta exceeds 100 in " + str(count_of_games_where_score_difference_is_big / n_matches))
  print("delta exceeds 250 in " + str(count_of_games_where_score_difference_is_big_3 / n_matches))
  #for snake_id, opponents in seen_opponents.items():
  #  sorted_snakes = [(x[0],snake_map[x[0]],x[1]) for x in sorted(opponents.items(), key=lambda x: x[1], reverse=True)]
  #  print("")
  #  print(snake_id, snake_map[snake_id], sorted_snakes)
  #  print("")


if __name__ == "__main__":
  main()
