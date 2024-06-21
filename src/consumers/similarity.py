import numpy as np
from scipy.sparse import csr_matrix
from scipy.spatial.distance import cosine

# Function to compute similarity between two sparse vectors
def compute_sparse_vector_similarity(features1, features2):
    print('features1=',features1)
    print('features2=',features2)
    #features2=features2['features']
   
    size = max(int(features1['size']), int(features2[0]))

    # Convert to sparse matrix format
    vec1 = csr_matrix((np.array(features1['values'], dtype=float),
                       (np.zeros(len(features1['indices'])), np.array(features1['indices'], dtype=int))), shape=(1, size))
    vec2 = csr_matrix((np.array(features2[2], dtype=float),
                       (np.zeros(len(features2[1])), np.array(features2[1], dtype=int))), shape=(1, size))

    # Compute cosine similarity
    similarity = 1 - cosine(vec1.toarray().flatten(), vec2.toarray().flatten())
    return similarity

def look_for_similarity(current_features,old_features,threshold=0.8):
    #print('current features=',current_features)
    #print('old features=',old_features)
    max_similarity=-2
    for features in old_features:
        similarity=compute_sparse_vector_similarity(current_features,features)
        if similarity>max_similarity:
            max_similarity=similarity
        #if similarity>=threshold:
            #return similarity
    return max_similarity


"""
# Test the function with two example vectors
features1 = {
    'indices': [0, 2, 4],
    'values': [1.0, 2.0, 3.0],
    'size': 5
}

features2 = {
    'indices': [0, 1, 4],
    'values': [1.0, 1.5, 2.5],
    'size': 5
}

features2 = {
    'indices': [0, 1, 4],
    'values': [1.0, 40, 2.5],
    'size': 5
}

# Compute and print the similarity
similarity = compute_sparse_vector_similarity(features1, features2)
print(f"Similarity between vectors: {similarity}")

# Test with current features and old features
current_features_list = [
    {
        'indices': [0, 2, 4],
        'values': [1.0, 2.0, 3.0],
        'size': 5
    },
    {
        'indices': [1, 3],
        'values': [0.5, 1.5],
        'size': 5
    },
    {
        'indices': [0, 1, 4],
        'values': [0.8, 2.1, 3.1],
        'size': 5
    }
]

old_features = [
    {
        'indices': [0, 1, 4],
        'values': [1.0, 1.5, 2.5],
        'size': 5
    },
    {
        'indices': [0, 1, 4],
        'values': [1.0, 40, 2.5],
        'size': 5
    },
    {
        'indices': [1, 3],
        'values': [0.4, 1.4],
        'size': 5
    }
]

# Compute and print similarities for current features against old features
for i, current_features in enumerate(current_features_list):
    similarity = look_for_similarity(current_features, old_features, threshold=0.8)
    if similarity:
        print(f"Current features {i+1} has a similar vector with similarity score: {similarity}")
    else:
        print(f"Current features {i+1} has no similar vector above the threshold")
"""