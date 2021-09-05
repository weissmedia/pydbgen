import os
import random
import sqlite3
from pathlib import Path
from random import randint, choice
import pandas as pd
from faker import Faker


class pydb:
    def __init__(self, seed=None, domain: Path=None, city: Path=None):
        """
        Initiates the class and creates a Faker() object for later data generation by other methods
        seed: User can set a seed parameter to generate deterministic, non-random output
        """

        self.faker = Faker
        self.fake = Faker()
        self.seed = seed
        self.randnum = randint(1, 9)

        self.city_list = self._initialize_city_list(city)
        self.domain_list = self._initialize_email_domain_list(domain)

    def _initialize_city_list(self, path: Path=None):
        if not path:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            path = dir_path + os.sep + "Cities.txt"

        with open(path) as fh:
            city_list = [str(line).strip() for line in fh.readlines()]

        return city_list

    def _initialize_email_domain_list(self, path: Path=None):
        if not path:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            path = dir_path + os.sep + "Domains.txt"

        with open(path) as fh:
            domain_list = [str(line).strip() for line in fh.readlines()]

        return domain_list

    def simple_ph_num(self, seed=None):
        """
        Generates 10 digit US phone number in xxx-xxx-xxxx format
        seed: Currently not used. Uses seed from the pydb class if chosen by user
        """
        random.seed(self.seed)

        phone_format = "{p1}-{p2}-{p3}"

        p1 = str(randint(100, 999))
        p2 = str(randint(0, 999)).rjust(3, "0")
        p3 = str(randint(0, 9999)).rjust(4, "0")

        return phone_format.format(p1=p1, p2=p2, p3=p3)

    def license_plate(self, seed=None, style=None):
        """
        Generates vehicle license plate number in 3 possible styles
        Style can be 1, 2, or 3.
        - 9ABC123 format
        - ABC-1234 format
        - ABC-123 format
        If style is not specified by user, a random style is chosen at runtime
        seed: Currently not used. Uses seed from the pydb class if chosen by user
        """
        random.seed(self.seed)

        if not style:
            style = choice([1, 2, 3])

        license_place_format = "{p1}{p2}{p3}"

        if style == 1:
            p1 = str(randint(1, 9))
            p2 = "".join([chr(randint(65, 90)) for _ in range(3)])
            p3 = "".join([str(randint(1, 9)) for _ in range(3)])
        elif style == 2:
            p1 = "".join([chr(randint(65, 90)) for _ in range(3)])
            p2 = "-"
            p3 = "".join([str(randint(0, 9)) for _ in range(4)])
        else:
            p1 = "".join([chr(randint(65, 90)) for _ in range(3)])
            p2 = "-"
            p3 = "".join([str(randint(0, 9)) for _ in range(3)])

        return license_place_format.format(p1=p1, p2=p2, p3=p3)

    def realistic_email(self, name, seed=None):
        """
        Generates realistic email from first and last name and a random domain address
        seed: Currently not used. Uses seed from the pydb class if chosen by user
        """
        random.seed(self.seed)

        name = str(name)
        f_name = name.split()[0]
        l_name = name.split()[-1]

        choice_int = choice(range(10))

        domain = choice(self.domain_list)

        name_formats = [
            "{f}{last}",
            "{first}{last}",
            "{first}.{l}",
            "{first}_{l}",
            "{first}.{last}",
            "{first}_{last}",
            "{last}_{first}",
            "{last}.{first}",
        ]
        name_fmt_choice = choice(name_formats)
        name_combo = name_fmt_choice.format(
            f=f_name[0], l=l_name[0], first=f_name, last=l_name
        )

        if choice_int < 7:
            email = name_combo + "@" + str(domain)
        else:
            random_int = randint(11, 99)
            email = name_combo + str(random_int) + "@" + str(domain)

        return email

    def city_real(self, seed=None):
        """
        Picks and returns a random entry out of 385 US cities
        seed: Currently not used. Uses seed from the pydb class if chosen by user
        """
        random.seed(self.seed)

        return choice(self.city_list)

    def gen_data_series(self, num=10, data_type="name"):
        """
        Returns a pandas series object with the desired number of entries and data type

        Data types available:
        - Name, country, city, real (US) cities, US state, zipcode, latitude, longitude
        - Month, weekday, year, time, date
        - Personal email, official email, SSN
        - Company, Job title, phone number, license plate

        Phone number can be two types:
        'phone_number_simple' generates 10 digit US number in xxx-xxx-xxxx format
        'phone_number_full' may generate an international number with different format

        seed: Currently not used. Uses seed from the pydb class if chosen by user

        """
        if type(data_type) != str:
            raise ValueError("Data type must be of type str, found " + str(type(data_type)))
        try:
            num = int(num)
        except:
            raise ValueError(f"Number of samples must be a positive integer, found {num}")

        if num <= 0:
            raise ValueError(f"Number of samples must be a positive integer, found {num}")

        num = int(num)
        fake = self.fake
        Faker.seed(self.seed)

        func_lookup = {
            "name": fake.name,
            "first_name": fake.first_name,
            "last_name": fake.last_name,
            "country": fake.country,
            "street_address": fake.street_address,
            "city": fake.city,
            "real_city": self.city_real,
            "state": fake.state,
            "zipcode": fake.zipcode,
            "latitude": fake.latitude,
            "longitude": fake.longitude,
            "name_month": fake.month_name,
            "weekday": fake.day_of_week,
            "year": fake.year,
            "time": fake.time,
            "date": fake.date,
            "ssn": fake.ssn,
            "email": fake.email,
            "office_email": fake.company_email,
            "company": fake.company,
            "job_title": fake.job,
            "phone_number_simple": self.simple_ph_num,
            "phone_number_full": fake.phone_number,
            "license_plate": self.license_plate,
        }

        if data_type not in func_lookup:
            raise ValueError("Data type must be one of " + str(list(func_lookup.keys())))

        datagen_func = func_lookup[data_type]
        return pd.Series((datagen_func() for _ in range(num)))

    def _validate_args(self, num, fields):
        try:
            num = int(num)
        except:
            raise ValueError(f"Number of samples must be a positive integer, found {num}")
        if num <= 0:
            raise ValueError(f"Number of samples must be a positive integer, found {num}")

        num_cols = len(fields)
        if num_cols < 0:
            raise ValueError("Please provide at least one type of data field to be generated")

    def gen_dataframe(self, num=10, fields=None, real_email=True, real_city=True, phone_simple=True):
        """
        Generate a pandas dataframe filled with random entries.
        User can specify the number of rows and data type of the fields/columns

        Data types available:
        - Name, country, city, real (US) cities, US state, zipcode, latitude, longitude
        - Month, weekday, year, time, date
        - Personal email, official email, SSN
        - Company, Job title, phone number, license plate

        Further choices are following:
        real_email: If True and if a person's name is also included in the fields, a realistic email will be generated corresponding to the name
        real_city: If True, a real US city's name will be picked up from a list. Otherwise, a fictitious city name will be generated.
        phone_simple: If True, a 10 digit US number in the format xxx-xxx-xxxx will be generated. Otherwise, an international number with different format may be returned.

        seed: Currently not used. Uses seed from the pydb class if chosen by user

        """
        if fields is None:
            fields = ["name"]
        self._validate_args(num, fields)

        df = pd.DataFrame(
            data=self.gen_data_series(num, data_type=fields[0]), columns=[fields[0]]
        )
        for col in fields[1:]:
            if col == "phone":
                if phone_simple:
                    df["phone-number"] = self.gen_data_series(
                        num, data_type="phone_number_simple"
                    )
                else:
                    df["phone-number"] = self.gen_data_series(
                        num, data_type="phone_number_full"
                    )
            elif col == "license_plate":
                df["license-plate"] = self.gen_data_series(num, data_type=col)
            elif col == "city" and real_city:
                df["city"] = self.gen_data_series(num, data_type="real_city")
            else:
                df[col] = self.gen_data_series(num, data_type=col)

        if ("email" in fields) and real_email:
            if "name" in fields:
                df["email"] = df["name"].apply(self.realistic_email)
            elif all(n in fields for n in ["first_name", "last_name"]):
                df["email"] = (df["first_name"] + " " + df["last_name"]).apply(self.realistic_email)

        return df

    def gen_table(
            self,
            num=10,
            fields=None,
            db_file=None,
            table_name=None,
            primarykey=None,
            real_email=True,
            real_city=True,
            phone_simple=True
    ):
        """
        Attempts to create a table in a database (.db) file using Python's built-in SQLite engine.
        User can specify various data types to be included as database table fields.
        All data types (fields) in the SQLite table will be of VARCHAR type.

        Data types available:
        - Name, country, city, real (US) cities, US state, zipcode, latitude, longitude
        - Month, weekday, year, time, date
        - Personal email, official email, SSN
        - Company, Job title, phone number, license plate

        Further choices are following:
        real_email: If True and if a person's name is also included in the fields, a realistic email will be generated corresponding to the name
        real_city: If True, a real US city's name will be picked up from a list. Otherwise, a fictitious city name will be generated.
        phone_simple: If True, a 10 digit US number in the format xxx-xxx-xxxx will be generated. Otherwise, an international number with different format may be returned.

        Default database and table name will be chosen if not specified by user.
        Primarykey: User can choose a PRIMARY KEY from among the data type fields. If nothing specified, the first data field will be made PRIMARY KEY.

        seed: Currently not used. Uses seed from the pydb class if chosen by user

        """
        if fields is None:
            fields = ["name"]
        self._validate_args(num, fields)

        if not db_file:
            conn = sqlite3.connect("NewFakeDB.db")
            c = conn.cursor()
        else:
            conn = sqlite3.connect(str(db_file))
            c = conn.cursor()

        if type(primarykey) != str and primarykey is not None:
            print("Primary key type not identified. Not generating any table")
            return None

        # If primarykey is None, designate the first field as primary key
        if not primarykey:
            table_cols = "(" + str(fields[0]) + " varchar PRIMARY KEY NOT NULL,"
            for col in fields[1:-1]:
                table_cols += str(col) + " varchar,"
            table_cols += str(fields[-1]) + " varchar" + ")"
            # print(table_cols)
        else:
            pk = str(primarykey)
            if pk not in fields:
                print(
                    "Desired primary key is not in the list of fields provided, cannot generate the table!"
                )
                return None

            table_cols = "(" + str(fields[0]) + " varchar, "
            for col in fields[1:-1]:
                if col == pk:
                    table_cols += str(col) + " varchar PRIMARY KEY NOT NULL,"
                else:
                    table_cols += str(col) + " varchar, "
            table_cols += str(fields[-1]) + " varchar" + ")"
            # print(table_cols)

        if not table_name:
            table_name = "Table1"
        else:
            table_name = table_name

        str_drop_table = f"DROP TABLE IF EXISTS {table_name};"
        c.execute(str_drop_table)
        str_create_table = "CREATE TABLE IF NOT EXISTS {table_name}{table_cols};"
        c.execute(str_create_table)

        # Create a temporary df
        temp_df = self.gen_dataframe(
            num=num,
            fields=fields,
            real_email=real_email,
            real_city=real_city,
            phone_simple=phone_simple,
        )
        # Use the dataframe to insert into the table
        for i in range(num):
            str_insert = (
                    "INSERT INTO "
                    + table_name
                    + " VALUES "
                    + str(tuple(temp_df.iloc[i]))
                    + ";"
            )
            c.execute(str_insert)

        # Commit the insertions and close the connection
        conn.commit()
        conn.close()

    def gen_excel(
            self,
            num=10,
            fields=None,
            filename="NewExcel.xlsx",
            real_email=True,
            real_city=True,
            phone_simple=True
    ):
        """
        Attempts to create an Excel file using Pandas excel_writer function.
        User can specify various data types to be included as fields.

        Data types available:
        - Name, country, city, real (US) cities, US state, zipcode, latitude, longitude
        - Month, weekday, year, time, date
        - Personal email, official email, SSN
        - Company, Job title, phone number, license plate

        Further choices are following:
        real_email: If True and if a person's name is also included in the fields, a realistic email will be generated corresponding to the name
        real_city: If True, a real US city's name will be picked up from a list. Otherwise, a fictitious city name will be generated.
        phone_simple: If True, a 10 digit US number in the format xxx-xxx-xxxx will be generated. Otherwise, an international number with different format may be returned.

        Default file name will be chosen if not specified by user.

        seed: Currently not used. Uses seed from the pydb class if chosen by user

        """
        if fields is None:
            fields = ["name"]
        self._validate_args(num, fields)

        # Create a temporary dataframe
        temp_df = self.gen_dataframe(
            num=num,
            fields=fields,
            real_email=real_email,
            real_city=real_city,
            phone_simple=phone_simple,
        )
        # Use the dataframe to write to an Excel file using Pandas built-in function
        temp_df.to_excel(filename)
