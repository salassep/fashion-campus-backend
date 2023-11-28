import sys
import uuid
import pathlib
from helpers import *

@grade
def home_test():
    with safe_init(1):
        sys.path.append(f'{pathlib.Path().resolve()}/Api/Flask')
        from main import app

        app.config.update({"TESTING": True})
        c = app.test_client()
    
    with Scorer(0.5, "2. Get banner"):
        banners = [
            {
                "id": str(uuid.uuid4()),
                "image": f"{get_random_string()}.jpg",
                "title": "testing_banner1"
            },
            {
                "id": str(uuid.uuid4()),
                "image": f"{get_random_string()}.jpg",
                "title": "testing_banner2"
            },
            {
                "id": str(uuid.uuid4()),
                "image": f"{get_random_string()}.jpg",
                "title": "testing_banner3"
            },
        ]

        # Delete data in the testing database with a title starting with testing_banner
        run_query("DELETE FROM banners WHERE title LIKE 'testing_banner%'")

        # Input the banner testing data into the testing database 
        run_query("INSERT INTO banners(id, image, title) VALUES(:id, :image, :title)", banners)

        banner_data = run_query(
            "SELECT id, image, title FROM banners WHERE deleted_at IS NULL", commit=False
        )

        # Get banners
        assert_response(
            c,
            "get",
            "/home/banner",
            exp_json = {
                "success": True,
                "data": banner_data
            },
            exp_code=200,
        )

    
    with Scorer(0.5, "3. Get category"):
        # Get category testing data from the testing database
        categories = run_query(
            "SELECT id, category_name AS title FROM categories WHERE deleted_at IS NULL", commit=False
        )

        for index, category in enumerate(categories):
            categories[index]["image"] = IsString()

        # Get categories
        assert_response(
            c,
            "get",
            "/home/category",
            exp_json = {
                "success": True,
                "data": IsIn(categories, "title")
            },
            exp_code=200,
        )

if __name__ == "__main__":
    highlight("Testing for home endpoint...")
    tests = [home_test]

    final_score = 0
    perfect_score = 0
    for test_f in tests:
        total_score, total_weight = test_f()
        final_score += total_score
        perfect_score += total_weight

    perc = round(final_score / perfect_score * 100, 1)
    result = f"{COL.PASS}Test passed! {COL.ENDC}" if perc == 100.0 else f"{COL.FAIL}Test failed! {COL.ENDC}"
    highlight(
        f"{COL.BOLD}YOUR Score for home endpoint: {COL.ENDC} "
        + f"{COL.BLUE}{final_score}/{perfect_score} ({perc}%){COL.ENDC} "
        + result
    )

    if perc != 100.0:
        raise Exception()