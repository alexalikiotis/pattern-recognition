from scipy.spatial import distance


def load(path, seperator):
    file_data = open(path, "r", encoding="ISO-8859-1").read().split("\n")
    normalized_data = []

    # Seperate data according to seperator
    for row in file_data:
        if row != "":
            normalized_data.append(row.split(seperator))

    return normalized_data


def create_users_vectors(ratings_data, users_data, movies_data):

    # Creating user vectors initialized with 0
    users_vectors = [[[0, 0] for x in range(0, 19)]
                     for y in range(0, len(users_data))]

    for rating in ratings_data:

        movie = movies_data[int(rating[1]) - 1][5:]

        for index, genre in enumerate(movie):
            if genre is "1":
                users_vectors[int(rating[0]) - 1][index][0] += int(rating[2])
                users_vectors[int(rating[0]) - 1][index][1] += 1

    # Finding the avg value of rating per movie genre per user
    for vector in users_vectors:
        for index, elem in enumerate(vector):
            if elem[1] is 0:
                elem = 0
            else:
                elem = round(elem[0] / elem[1])
            vector[index] = elem

    return users_vectors


def find_min_max_distances(vectors):
    dist = []

    # Finding the min,max euclidian distances of the vectors
    for i in range(len(vectors)):
        for j in range(i+1, len(vectors)):
            dist.append(distance.euclidean(vectors[i], vectors[j]))
    return min(dist), max(dist)


class Bsas:
    def find_clusters(vectors, theta, max_clusters):
        clusters = [[vectors[0]]]

        for vector in vectors[1:]:

            # Calculating the distances from each cluster
            dist = []
            for cluster in clusters:
                sub_dist = [
                    distance.euclidean(vector, c_vec) for c_vec in cluster
                ]

                dist.append(min(sub_dist))

            # Finding the smallest one
            min_dist = min(dist)

            # Getting the index of the selected cluster
            index = dist.index(min(dist))

            if min_dist > theta and len(clusters) < max_clusters:
                # Create new cluster
                clusters.append([vector])
            else:
                # Append vector to cluster
                clusters[index].append(vector)

        return clusters


ratings = load("data/u.data", "\t")
users = load("data/u.user", "|")
movies = load("data/u.item", "|")

vectors = create_users_vectors(ratings, users, movies)

min_distance, max_distance = find_min_max_distances(vectors)

# Calculating theta upper and lower limits from formula
theta_min = min_distance + 0.25 * (max_distance - min_distance)
theta_max = min_distance + 0.75 * (max_distance - min_distance)
