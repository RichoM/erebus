# MapScorer.py - Alfred Roberts 2021

# Helper functions to be used within
# the MainSupervisor to give points
# to teams for the outputted map
# matrix.

# NOT FULLY IMPLEMENTED!!!!
# THIS IS TEST CODE ONLY

import numpy as np

def _get_answer_matrix(map: int) -> np.array:
    """
    Get answer matrix from map

    For now, I'm just returning a constant matrix
    """
    answer_matrix = np.array([
        [0,0,1,5,1,0,0,0,1,5,1],
        [0,0,1,5,1,0,0,0,1,5,1],
        [0,0,1,5,1,1,1,1,1,5,1],
        [0,0,1,3,3,3,3,3,3,3,1],
        [1,1,1,3,1,1,1,3,3,3,1],
        [1,3,1,3,1,3,1,3,3,3,1],
        [1,3,1,3,1,3,1,1,1,3,1],
        [1,3,3,3,3,3,2,2,2,3,1],
        [1,1,1,1,1,1,1,1,1,1,1]
    ])
    return answer_matrix

def _get_first_connector_instance(matrix: np.array) -> np.array:
    n,m = matrix.shape
    for y in range(n):
        for x in range(m):
            if matrix[y,x] == 5:
                return np.array([y,x])

def _shift_matrix(answerMatrix: np.array, subMatrix: np.array, dy: int, dx: int) -> np.array:
    n,m = subMatrix.shape
    an,am = answerMatrix.shape

    bigSubMatrix = np.zeros((n *3,m *3),subMatrix.dtype) 
    bigSubMatrix[n:2*n,m:2*m] = subMatrix

    x = m - (dx)
    y = n - (dy)
    return bigSubMatrix[y:y+an, x:x+am]
    

def _align(answerMatrix: np.array, subMatrix: np.array) -> np.array:
    """
    Align the subMatrix with the answerMatrix via one of the connectors

    Returns:
        subMatrix aligned with the answerMatrix
    """
    ans_con_pos = _get_first_connector_instance(answerMatrix)
    sub_con_pos = _get_first_connector_instance(subMatrix)
    d_pos = ans_con_pos - sub_con_pos

    return _shift_matrix(answerMatrix, subMatrix,*d_pos)


# def _get_same_orientation(answerMatrix: np.array, subMatrix: np.array) -> np.array:
#     """
#     Rotate the subMatrix to fit the same orientation as the answerMatrix

#     Returns:
#         subMatrix rotated (np array)
#     """
#     if answerMatrix.shape == subMatrix.shape:
#         return subMatrix
#     # else
#     # TODO Could be upside down??
#     while True:
#         subMatrix = np.rot90(subMatrix, k=1, axes=(1,0))
#         if answerMatrix.shape == subMatrix.shape:
#             return subMatrix

def _calculate_completeness(answerMatrix: np.array, subMatrix: np.array) -> float:
    """
    Calculate the quatifiable completeness score of a matrix, compared to another

    Args:
        answerMatrix (np.array): answer matrix to check against
        subMatrix (np.array): matrix to compare

    Returns:
        float: completeness score
    """
    correct = 0
    incorrect = 0


    if answerMatrix.shape != subMatrix.shape:
        return 0

    for i in range(len(answerMatrix)):
        for j in range(len(answerMatrix[0])):
            # If the cells are equal
            a = (subMatrix[i][j] == answerMatrix[i][j])
            if a:
                correct += 1
            else:
                incorrect += 1

    # Calculate completeness as a ratio of the correct count over the sum of the correct count and incorrect count 
    completeness = (correct / (correct + incorrect))

    return completeness

def _calculate_map_completeness(map: int, subMatrix: np.array) -> float:
    """
    Calculate completeness of submitted map area matrix

    Args:
        map (int): specifies which map to score
        subMatrix (np array): team submitted array
    """
    answerMatrix = _get_answer_matrix(map) 

    completeness_list = []

    for i in range(0,4):
        answerMatrix = np.rot90(answerMatrix,k=i,axes=(1,0))
        aSubMatrix = _align(answerMatrix,subMatrix)


        # Calculate score for matrix
        completeness = _calculate_completeness(answerMatrix, aSubMatrix)
        completeness_list.append(completeness)
    # Return the highest score
    return max(completeness_list)

    

def calculateScore(answerMatrices: list, subMatrix: np.array) -> float:
    subMatrix = np.rot90(subMatrix,k=0,axes=(1,0))

    score = 0
    # Map 1
    score += _calculate_map_completeness(answerMatrices[0],subMatrix)
    # Map 2
    score += _calculate_map_completeness(answerMatrices[1],subMatrix)
    # Map 3
    score += _calculate_map_completeness(answerMatrices[2],subMatrix)
    # Score as an average of the completeness of all the maps
    return score / 3

if __name__ == "__main__":
    subMatrix = np.array([
        [0,0,0,1,5,1,0,0,0,1,5,1],
        [0,0,0,1,5,1,0,0,0,1,5,1],
        [0,0,0,1,5,1,1,1,1,1,5,1],
        [0,0,0,1,3,3,3,3,3,3,3,1],
        [0,1,1,1,3,1,1,1,3,3,3,1],
        [0,1,3,1,3,1,3,1,3,3,3,1],
        [0,1,3,1,3,1,3,1,1,1,3,1],
        [0,1,3,3,3,3,3,2,2,2,3,1],
        [0,1,1,1,1,1,1,1,1,1,1,1]
    ])
    
