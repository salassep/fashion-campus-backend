
# Fashion Campus

The Campus Fashion Company presents a catalog of local to international brands that are loved by young people. Because we work a lot with local brands, after operating for more than a year.

They found that during this pandemic new trends emerged among the Fashion Campus target market. Apparently, "Indonesian Young Urbans" began to practice thrifting or buying and selling used clothes.


![Logo](http://34.143.167.23:5000/image/banner-1.jpg)


## BE EightWeeks

- [@yovixtar](https://gitlab.com/yovixtar) - Khazim Fikri Al-Fadhli
- [@salassep](https://gitlab.com/salassep) - Salas Sepkardianto


## Resource

 - [GitLab Backend](https://gitlab.com/yovixtar/final-project-eightweeks)
 - [GitLab Frontend](https://gitlab.com/yovixtar/final-project-frontend)
 - [ERD](https://lucid.app/lucidchart/4eeacc26-027e-4677-a365-928518164ade/edit?viewport_loc=-1440%2C-430%2C5679%2C2665%2C0_0&invitationId=inv_8d8cc50d-0055-44e4-8c95-64d4c42ef554)
 - [Backend URL](http://34.143.167.23:5000/)
 - [Frontend URL](http://34.143.167.23:3000/)
 - [Adminer - Database Manager](http://34.143.167.23:8080/)
 

## Tech Stack

**Client:** React

**Server:** Google Cloud, Docker, Flask (Python), PostgreSQL (SQLAlchemy)

**Git Repository:** GitLab

![Logo](http://34.143.167.23:5000/image/readme-tech-tools.png)


## Installation

1. Clone project BE to your work directory

```bash
  git clone https://gitlab.com/yovixtar/final-project-eightweeks.git
```

2. Clone project FE to your work directory

```bash
  git clone https://gitlab.com/yovixtar/final-project-frontend.git
```
    
3. Open your work directory FE Project, Change .env BACKEND_URL to your server ip/your host to use this app

```bash
  BACKEND_URL=http://yourhost:5000
```
    
4. Run docker compose in BE and FE project work directory

```bash
  docker compose up -d --build
```
    
5. Populate/model data is automated added, helper insert population/model data is in a following link

```bash
  http://yourhost:5000/helper-insert
```


## Running Tests

Change os environment in file `/Api/Flask/util/db.py` :

```python
    os.environ["POSTGRES_USER"],        >>  "your_postgres_user"
    os.environ["POSTGRES_PASSWORD"],    >>  "your_postgres_user's_password"
    os.environ["POSTGRES_HOST"],        >>  "db-postgres"     (container name)
    os.environ["POSTGRES_PORT"],        >>  5432              (or your postgres posrt)
    os.environ["POSTGRES_DB"],          >>  "fashioncampus"
```

To run tests, run the following command

Before Script:

```bash
  python --version # For debugging
  python3.9 -m pip install virtualenv
  python3.9 -m venv $ENVIRONMENT_NAME
  source $ENVIRONMENT_NAME/bin/activate
  python3.9 -m pip install -r Api/req.txt
  pwd && ls # for debugging
```

```bash
  python3.9 Api/Tests/universal_test.py
  python3.9 Api/Tests/home_test.py
  python3.9 Api/Tests/auth_test.py
  python3.9 Api/Tests/product_list_test.py
  python3.9 Api/Tests/product_detail_test.py
  python3.9 Api/Tests/cart_test.py
  python3.9 Api/Tests/profile_test.py
  python3.9 Api/Tests/admin_test.py
```


## Features

- Authentication (Buyer and Seller)
- Search and Filter Product List
- Show banner & Category
- Buyer Carts
- Buyer's information management
- Buyer's Balance
- Calculate shipping price
- Product management
- Category management
- Order list
- Calculate total sales
- Change status buyer's order (Waiting, Processed, Delivered, Arrived)
- Buyer confirmation received order
- Buyer's Wishlist
- Recommend similar product
- Show popular product
- Show Status Product & Category
- Status Product & Category management
- Banner management


## License

Copyright (c) [2022] [EightWeeks Team]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Fashion Campus"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[MIT licenses](https://choosealicense.com/licenses/mit/)

