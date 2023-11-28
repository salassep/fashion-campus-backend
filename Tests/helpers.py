import traceback
from functools import wraps
from random import choice, choices, randint, shuffle
from string import ascii_lowercase, ascii_uppercase, digits

###################################################################################
#                                   GRADE HELPERS
###################################################################################
def grade(f: callable):
    @wraps(f)
    def dec(*args, **kwargs):
        global MAX_SCORE, FINAL_SCORE
        MAX_SCORE, FINAL_SCORE = 0, 0
        try:
            f(*args, **kwargs)
        finally:
            res = FINAL_SCORE, MAX_SCORE
            # reset final score before returning
            FINAL_SCORE = 0
            return res

    return dec


def assert_eq_dict(expression, expected: dict) -> bool:
    if not isinstance(expression, dict):
        return False

    for k in expected:
        if k not in expression:
            return False

    for k, v in expression.items():
        if k not in expected:
            return False
        if v != expected[k]:
            return False

    return True


def assert_eq(
    expression, expected, exc_type=AssertionError, hide: bool = False, err_msg=None
):
    try:
        if isinstance(expected, dict):
            if assert_eq_dict(expression, expected):
                return
        elif expression == expected:
            return

        errs = [err_msg] if err_msg else []
        if hide:
            expected = "<hidden>"
        err = "\n".join([*errs, f"> Expected: {expected}", f"> Yours: {expression}"])
        raise exc_type(err)
    except Exception:
        raise

class Scorer:
    def __enter__(self):
        pass

    def __init__(self, score: float, desc: str):
        self.score = score
        global MAX_SCORE
        MAX_SCORE += score
        print(f"{COL.BOLD}{desc}{COL.ENDC} ({self.score} pts)")

    def __exit__(self, exc_type, exc_value, exc_tb):
        # add maximum score when passing these statements, otherwise 0
        if not exc_type:
            global FINAL_SCORE
            FINAL_SCORE += self.score
            print(COL.PASS, f"\tPASS: {self.score} pts", COL.ENDC)
        else:
            err_lines = [exc_type.__name__, *str(exc_value).split("\n")]
            errs = [
                "\t" + (" " * 4 if index else "") + line
                for index, line in enumerate(err_lines)
            ]
            print("{}{}".format(COL.WARNING, "\n".join(errs)))
            print(f"\t{COL.FAIL}FAIL: 0 pts", COL.ENDC)

        # skip throwing the exception
        return True

class safe_init:
    def __enter__(self):
        pass

    def __init__(self, max_score: int):
        self.max_score = max_score

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type:
            print(traceback.format_exc())
            global MAX_SCORE
            MAX_SCORE = self.max_score
            return False

        return True

def assert_response(
    c,
    method: str,
    endpoint: str,
    json: dict = None,
    exp_json=None,
    exp_code: int = None,
    headers: dict = None,
    exp_content_type: str = None
):
    if not headers:
        headers = {}

    response = getattr(c, method)(endpoint, json=json, headers=headers)
    if exp_json and exp_code:
        assert_eq(response.json, exp_json)
        assert_eq(response.status_code, exp_code)
    
    if exp_content_type:
        assert_eq(response.headers["Content-Type"], exp_content_type)

    return response.json

###################################################################################
#                             DISPLAY RESULT HELPERS
###################################################################################
# https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
class COL:
    PASS = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    BLUE = "\033[94m"
    UNDERLINE = "\033[4m"

# special exception when something should've been printed, but wasn't
class DisplayError(Exception):
    pass

def highlight(s: str):
    print("=" * 29 + "\n")
    print(s)
    print("\n" + "=" * 29)

###################################################################################
#                            CHECK DATA TYPE HELPERS
###################################################################################
class IsString:
    def __eq__(self, other):
        return isinstance(other, str)

    def __repr__(self):
        return "<must_be_a_string>"

class IsIn:
    def __init__(self, data: list, identifier: str):
        self.data = data
        self.identifier = identifier

    def __eq__(self, other):
        if not isinstance(other, list):
            return False

        for item in other:
            filtered_data = list(
                filter(
                    lambda data: data[self.identifier] == item[self.identifier], self.data
                )
            )

            if not filtered_data:
                return False

            for key in item.keys():
                if item[key] != filtered_data[0][key]:
                    return False
                
        return True

    def __repr__(self):
        return "<must_match_the_sample_data>"

class IsMatch(IsIn):
    def __eq__(self, other):
        if not isinstance(other, list):
            return False

        if len(self.data) != len(other):
            return False

        for item in other:
            filtered_data = list(
                filter(
                    lambda data: data[self.identifier] == item[self.identifier], self.data
                )
            )

            if not filtered_data:
                return False

            for key in item.keys():
                if item[key] != filtered_data[0][key]:
                    return False
                
        return True

###################################################################################
#                          GENERATOR HELPERS
###################################################################################
def gen_password():
    # representative from each
    num = choice(digits)
    lower = choice(ascii_lowercase)
    upper = choice(ascii_uppercase)
    remaining = choices(
        [*digits, *ascii_lowercase, *ascii_uppercase], k=5 + randint(0, 5)
    )

    all_chars = [num, lower, upper, *remaining]
    shuffle(all_chars)
    res = "".join(all_chars)
    return res

def get_random_string():
    return ''.join(choice(ascii_lowercase) for _ in range(5))

def get_random_number():
    return ''.join(choice(digits) for _ in range(8))

###################################################################################
#                           DATABASE HELPERS
###################################################################################
def run_query(query: str, data: list = [], commit: bool = True):
    """Runs a query against the given postgresql database"""

    from sqlalchemy import create_engine, text

    # credential for development only
    engine_uri = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        "jeezy",
        "jeezy",
        "35.240.159.32",
        4321,
        "fp_dev",
    )

    engine = create_engine(engine_uri, future=True)
    if isinstance(query, str):
        query = text(query)

    with engine.connect() as conn:
        if not commit:
            return [dict(row) for row in conn.execute(query)]
        if data:
            conn.execute(query, data)
        else:
            conn.execute(query)
        conn.commit()


def sign_in_as_admin(client, is_registered: bool = True):
    admin = {
        "name": "Admin",
        "email": "admin@gmail.com",
        "phone_number": f"0856{get_random_number()}",
        "password": "Admin123_",
        "type": "seller",
    }

    if not is_registered:
        assert_response(
            client,
            "post",
            "/sign-up",
            json=admin,
        )

    response = assert_response(
        client,
        "post",
        "/sign-in",
        json={ "email": admin["email"], "password": admin["password"] },
    )

    if not response["success"]:
        return sign_in_as_admin(client, False)

    return response['token']

    
def sign_in_as_buyer(client, is_registered: bool = True):
    tokens = []
    buyers = [
        {
            "name": "buyer1",
            "email": "buyer1@gmail.com",
            "phone_number": f"0856{get_random_number()}",
            "password": "Buyer123_",
        },
        {
            "name": "buyer2",
            "email": "buyer2@gmail.com",
            "phone_number": f"0856{get_random_number()}",
            "password": "Buyer123_",
        },
    ]

    if not is_registered:
        for buyer in buyers:        
            res = assert_response(
                client,
                "post",
                "/sign-up",
                json=buyer,
            )

    for buyer in buyers:
        response = assert_response(
            client,
            "post",
            "/sign-in",
            json={ "email": buyer["email"], "password": buyer["password"] },
        )

        if not response["success"]:
            return sign_in_as_buyer(client, False)
        
        tokens.append(response["token"])

    return tokens

def add_products_to_testing_db(data: list = None) -> list:
    from uuid import uuid4

    # Get categories from testing database
    categories = run_query(
        "SELECT id, category_name FROM categories WHERE deleted_at IS NULL LIMIT 2", commit=False
    )

    product_samples = data

    if not product_samples:
        product_samples = [
            (uuid4(), "Baju Merah", "description product", [], "used", categories[0]["id"], 1000),
            (uuid4(), "Celana Jeans", "description product", ["images_p4.png"], "used", categories[1]["id"], 3000)
        ]

    # Insert data product to testing database
    for id, product_name, description, images, condition, category_id, price in product_samples:
        run_query(
            "INSERT INTO products(id, category_id, product_name, description, condition, price) "\
            f"VALUES('{id}', '{category_id}' ,'{product_name}', '{description}', '{condition}', {price})"
        )

        if images:
            for image in images:
                run_query(
                    "INSERT INTO product_images(id, product_id, image) "\
                    f"VALUES('{uuid4()}', '{id}', '{image}')"
                )
    
    return product_samples

def add_carts_to_testing_db(user_id):
    from uuid import uuid4

    product_samples = add_products_to_testing_db()

    run_query(f"UPDATE carts SET deleted_at = now() WHERE user_id = '{user_id}'")

    products_to_cart = [
        {
            "id": uuid4(),
            "product_id": product_samples[0][0],
            "quantity": 2,
            "size": "M",
            "user_id": user_id
        },
        {
            "id": uuid4(),
            "product_id": product_samples[1][0],
            "quantity": 3,
            "size": "S",
            "user_id": user_id
        }
    ]

    for product in products_to_cart:
        run_query(
            "INSERT INTO carts(id, product_id, quantity, size, user_id) "\
            "VALUES(:id, :product_id, :quantity, :size, :user_id)", 
            product
        )

    return product_samples, products_to_cart