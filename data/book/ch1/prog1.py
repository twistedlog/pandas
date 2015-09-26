from __future__ import division
from collections import Counter
from collections import defaultdict

from data import users
from data import friendships
from data import interests


for user in users:
    user['friends'] = []


for i, j in friendships:
    users[i]['friends'].append(users[j])
    users[j]['friends'].append(users[i])


def number_of_friends(user):
    return len(user['friends'])


total_connections = sum(number_of_friends(user) for user in users)

num_users = len(users)
avg_connections = total_connections / num_users
print avg_connections

# find the most connected people
num_friends_by_id = [(user['id'], number_of_friends(user)) for user in users]
print sorted(num_friends_by_id, key=lambda (user_id, num_friends): num_friends, reverse=True)


def not_the_same(user, other_user):
    """Two users are not the same if they have the same ids"""
    return user["id"] != other_user["id"]


def not_firends(user, other_user):
    return all(not_the_same(friend, other_user) for friend in user['friends'])


def not_user_friends(user, friend):
    return not friend['id'] in [f['id'] for f in user['friends']]


def friend_of_friends(user):
    total = Counter(foaf['id']
                    for friend in user['friends']
                    for foaf in friend['friends']
                    if not_user_friends(user, foaf)
                    and not_the_same(user, foaf))
    return total

print friend_of_friends(users[3])


def data_scientists_who_like(target_interest):
    return [user_id for user_id, user_interest in interests
            if user_interest == target_interest]


user_ids_by_interest = defaultdict(list)

for user_id, interest in interests:
    user_ids_by_interest[interest].append(user_id)

# another index from user->interest

interests_by_user_id = defaultdict(list)
for user_id, interest in interests:
    interests_by_user_id[user_id].append(interest)


def most_common_interests_with(user):
    return Counter(interested_user_id
                   for interest in interests_by_user_id[user['id']]
                   for interested_user_id in user_ids_by_interest[interest]
                   if interested_user_id != user['id'])
