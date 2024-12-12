import json
import sys, os
from os import listdir
from os.path import isfile, join

# HACK(Richo)
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "game", "controllers", "MainSupervisor"))
from MapAnswer import MapAnswer

def compare_files(p1, p2):
    s1 = ""
    s2 = ""
    with open(p1, "r") as f:
        s1 = f.read()
    with open(p2, "r") as f:
        s2 = f.read()
    
    return s1 == s2

def test(world):
    data = None
    with open(f"test/{world}_map.json", "r") as f:
        data = json.load(f)
    
    mapa = MapAnswer.from_dict(data)
    actual = mapa.generateAnswer(False)

    with open(f"test/{world}_actual.txt", "w") as f:
        for row in actual:
            for col in row:
                f.write(col)
            f.write("\n")
    
    is_success = compare_files(f"test/{world}_expected.txt", f"test/{world}_actual.txt")
    if is_success:
        print(f"{world} -> SUCCESS")
    else:
        print(f"{world} -> FAILURE !!!!!!!!!!!!!!!!!!!!")
    
    return is_success

def listfiles(mypath):
    return [f for f in listdir(mypath) if isfile(join(mypath, f))]

def test_all_maps():
    files = listfiles("test")
    success_count = 0
    total_count = 0
    for file in files:
        if file.endswith("_map.json"):
            total_count += 1
            is_success = test(file.removesuffix("_map.json"))
            if is_success:
                success_count += 1

    print()
    print(f"{success_count} / {total_count} passed.")
    print(f"Failures: {total_count - success_count}")

test_all_maps()
# test("R1")