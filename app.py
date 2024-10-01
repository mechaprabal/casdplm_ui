import mariadb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from flask import Flask, render_template, request

app = Flask(__name__)


def db_query(
    db_username: str,
    db_pass: str,
    db_hostname: str,
    db_port: int,
    db_name: str,
    user_query: str,
):
    """
    This function can connect and manage the connection with
    MariaDB server
    """
    try:
        conn = mariadb.connect(
            user=db_username,
            password=db_pass,
            host=db_hostname,
            port=db_port,
            database=db_name,
        )

        print("connection succesful")

        # Execute the user query
        cur = conn.cursor()

        cur.execute(user_query)

        rows = cur.fetchall()

        # for row in rows:
        #     print(row)

        # fetch column names
        column_names = [i[0] for i in cur.description]

        # convert to pandas dataframe
        df = pd.DataFrame(rows, columns=column_names)

        # print statistics
        max_val = np.max(df.iloc[:, 3:].values[0])
        min_val = np.min(df.iloc[:, 3:].values[0])
        mean_val = np.mean(df.iloc[:, 3:].values[0])

    except mariadb.Error as e:
        print(f"Error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

    return (min_val, max_val, mean_val, df.iloc[:, 3:].values[0])


def build_chart(yearly_data):
    """
    This function will create a chart based
    on the data fetched from the database.
    """
    fig, ax = plt.subplots()

    ax.plot(
        list(range(1990, 2022, 1)),
        yearly_data,
    )

    ax.set_title("Annual Emissions")
    ax.set_xlabel("Year")
    ax.set_ylabel("Emissions")

    fig.savefig(
        "./static/annual_emissions.png",
        bbox_inches="tight",
        dpi=300,
    )

    return fig


@app.route("/", methods=["GET", "POST"])
def home():
    """
    Homepage of the app
    """

    if request.method == "POST":
        # perform the operations required on the user input

        form_res = request.form

        country_name = form_res.get("country_select")
        source_name = form_res.get("sector_select")
        gas_name = form_res.get("gas_select")

        user_selection_dict = {
            "country": country_name,
            "source": source_name,
            "gas": gas_name,
        }

        print(user_selection_dict)

        user_query = f"select * from historical_data where country='{country_name}' and sector='{source_name}' and gas='{gas_name}'"

        min_val, max_val, mean_val, yearly_data = db_query(
            db_username="root",
            db_pass="root123",
            db_hostname="localhost",
            db_port=3306,
            db_name="cw_emissions",
            user_query=user_query,
        )

        fig = build_chart(yearly_data=yearly_data)

        stats_dict = {"min": min_val, "max": max_val, "mean": mean_val}

        return render_template(
            "index.html",
            user_selection_dict=user_selection_dict,
            stats_dict=stats_dict,
            user_selection_toggle=1,
            chart_gen=1,
        )

    else:
        return render_template(
            "index.html",
            user_selection_toggle=0,
        )


@app.route("/about", methods=["GET"])
def about():
    """
    About the application
    """
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
