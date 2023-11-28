import sys
import pathlib
from helpers import *

@grade
def universal_test():
    with safe_init(4):
        sys.path.append(f'{pathlib.Path().resolve()}/Api/Flask')
        from main import app

        app.config.update({"TESTING": True})
        c = app.test_client()

    exist_image = ["white-ubuntu.png"]
    with Scorer(1, "1. Get image"):
        # Get picture that exist
        assert_response(
            c,
            "get",
            f"/image/{exist_image[0]}",
            exp_content_type="image/png",
        )

        # Get picture that unexist
        assert_response(
            c,
            "get",
            "/image/white-ubuntu.jpg",
            exp_json={"message": "error, Image not found", 'success': False},
            exp_code=404,
        )
    
if __name__ == "__main__":
    highlight("Testing for universal endpoint...")
    tests = [universal_test]

    final_score = 0
    perfect_score = 0
    for test_f in tests:
        total_score, total_weight = test_f()
        final_score += total_score
        perfect_score += total_weight

    perc = round(final_score / perfect_score * 100, 1)
    result = f"{COL.PASS}Test passed! {COL.ENDC}" if perc == 100.0 else f"{COL.FAIL}Test failed! {COL.ENDC}"
    highlight(
        f"{COL.BOLD}YOUR Score for universal endpoint: {COL.ENDC} "
        + f"{COL.BLUE}{final_score}/{perfect_score} ({perc}%){COL.ENDC} "
        + result
    )

    if perc != 100.0:
        raise Exception()