import sys
import pathlib
import uuid
from helpers import *

@grade
def product_list_test():
    with safe_init(2):
        sys.path.append(f'{pathlib.Path().resolve()}/Api/Flask')
        from main import app

        app.config.update({"TESTING": True})
        c = app.test_client()
    
    # Get category data from testing database
    categories = run_query(
        "SELECT id, category_name as title FROM categories WHERE deleted_at IS NULL", commit=False
    )

    with Scorer(1, "6. Get Product List"):
        # Delete data product in testing database
        run_query("UPDATE products SET deleted_at = now()")

        # Get product list with no data
        assert_response(
            c,
            "get",
            f"/products?page=1&page_size=2",
            exp_json={
                "success": True,
                "data": [],
                "total_rows": 0
            },
            exp_code=200
        )
        
        # Insert data product to testing database
        product_samples = add_products_to_testing_db()

        # Get products sort by from lower to higher price
        assert_response(
            c,
            "get",
            f"/products?page=1&page_size=100&sort_by=Price a_z",
            exp_json={
                "success": True,
                "data": [
                    {
                        "id": str(product_samples[0][0]),
                        "image": IsString(),
                        "title": product_samples[0][1],
                        "price": product_samples[0][6]
                    },
                    {
                        "id": str(product_samples[1][0]),
                        "image": IsString(),
                        "title": product_samples[1][1],
                        "price": product_samples[1][6]
                    },
                ],
                "total_rows": 2
            },
            exp_code=200
        )

        # Get products filter by price
        assert_response(
            c,
            "get",
            f"/products?page=1&page_size=100&sort_by=Price a_z&price=0,2500",
            exp_json={
                "success": True,
                "data": [
                    {
                        "id": str(product_samples[0][0]),
                        "image": IsString(),
                        "title": product_samples[0][1],
                        "price": product_samples[0][6]
                    },
                ],
                "total_rows": 1
            },
            exp_code=200
        )

        # Get products by categories
        assert_response(
            c,
            "get",
            f"/products?page=1&page_size=100&sort_by=price z_a&category={categories[0]['id']},{categories[1]['id']}",
            exp_json={
                "success": True,
                "data": [
                    {
                        "id": str(product_samples[1][0]),
                        "image": IsString(),
                        "title": product_samples[1][1],
                        "price": product_samples[1][6]
                    },
                    {
                        "id": str(product_samples[0][0]),
                        "image": IsString(),
                        "title": product_samples[0][1],
                        "price": product_samples[0][6]
                    },
                ],
                "total_rows": 2
            },
            exp_code=200
        )

        # Get a product
        assert_response(
            c,
            "get",
            f"/products?page=1&page_size=1&sort_by=price a_z",
            exp_json={
                "success": True,
                "data": [
                    {
                        "id": str(product_samples[0][0]),
                        "image": IsString(),
                        "title": product_samples[0][1],
                        "price": product_samples[0][6]
                    },
                ],
                "total_rows": 1
            },
            exp_code=200
        )

        # Get products using all filter
        assert_response(
            c,
            "get",
            f"/products?page=1&page_size=1&sort_by=price a_z&category={categories[0]['id']}&price=0,2500"\
            "&condition=used&product_name=Baju",
            exp_json={
                "success": True,
                "data": [
                    {
                        "id": str(product_samples[0][0]),
                        "image": IsString(),
                        "title": product_samples[0][1],
                        "price": product_samples[0][6]
                    },
                ],
                "total_rows": 1
            },
            exp_code=200
        )

    with Scorer(0.5, "7. Get Category"):
        # Get categories
        assert_response(
            c,
            "get",
            "/categories",
            exp_json={
                "success": True,
                "data": IsIn(categories, "title")
            },
            exp_code=200,
        )
    
    with Scorer(1, "8. Search Product by Image"):
        pass

if __name__ == "__main__":
    highlight("Testing for product list endpoint...")
    tests = [product_list_test]

    final_score = 0
    perfect_score = 0
    for test_f in tests:
        total_score, total_weight = test_f()
        final_score += total_score
        perfect_score += total_weight

    perc = round(final_score / perfect_score * 100, 1)
    result = f"{COL.PASS}Test passed! {COL.ENDC}" if perc == 100.0 else f"{COL.FAIL}Test failed! {COL.ENDC}"
    highlight(
        f"{COL.BOLD}YOUR Score for product list endpoint: {COL.ENDC} "
        + f"{COL.BLUE}{final_score}/{perfect_score} ({perc}%){COL.ENDC} "
        + result
    )

    if perc != 100.0:
        raise Exception()