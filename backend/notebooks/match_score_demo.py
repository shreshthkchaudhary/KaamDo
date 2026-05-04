"""
Match Score Demo — Weighted Formula Demo
=========================================
Shows the worker match scoring formula on 5 example workers.
Run: python match_score_demo.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from ai.match_score import calculate_match_score, haversine

# Example task
task = {
    'category': 'home repair',
    'lat': 12.9716,
    'lng': 77.5946,
    'radius_km': 5
}

# 5 example workers with varying attributes
workers = [
    {'name': 'Rahul', 'skills': 'home repair, plumbing', 'avg_rating': 4.8,
     'lat': 12.9750, 'lng': 77.5980, 'total_tasks': 45},
    {'name': 'Priya', 'skills': 'cleaning, home repair', 'avg_rating': 4.2,
     'lat': 12.9600, 'lng': 77.5800, 'total_tasks': 12},
    {'name': 'Amit', 'skills': 'tech help, education', 'avg_rating': 4.9,
     'lat': 12.9800, 'lng': 77.6100, 'total_tasks': 80},
    {'name': 'Sunita', 'skills': 'home repair', 'avg_rating': 3.5,
     'lat': 12.9500, 'lng': 77.5700, 'total_tasks': 5},
    {'name': 'Deepak', 'skills': 'labour & moving, home repair', 'avg_rating': 4.5,
     'lat': 13.0000, 'lng': 77.6200, 'total_tasks': 100},
]

print("="*70)
print("WORKER MATCH SCORE DEMO")
print(f"Task: '{task['category']}' at ({task['lat']}, {task['lng']}), radius {task['radius_km']}km")
print("="*70)

results = []
for w in workers:
    score = calculate_match_score(w, task)
    dist = haversine(w['lat'], w['lng'], task['lat'], task['lng'])
    results.append({'name': w['name'], 'score': score, 'distance': round(dist, 2),
                    'skills': w['skills'], 'rating': w['avg_rating'], 'tasks': w['total_tasks']})

results.sort(key=lambda x: x['score'], reverse=True)

print(f"\n{'Rank':<6}{'Name':<10}{'Score':<8}{'Distance':<10}{'Rating':<8}{'Tasks':<8}{'Skills'}")
print("-"*70)
for i, r in enumerate(results, 1):
    print(f"{i:<6}{r['name']:<10}{r['score']:<8}{r['distance']}km{'':<4}{r['rating']:<8}{r['tasks']:<8}{r['skills']}")

print(f"\nFormula: score = category_match*0.40 + rating*0.30 + proximity*0.20 + experience*0.10")
print(f"Best match: {results[0]['name']} with score {results[0]['score']}")
