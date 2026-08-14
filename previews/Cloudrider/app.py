from flask import Flask, render_template, request, redirect, url_for, flash
import os
import smtplib

from email.message import EmailMessage
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "cloudrider-development-key")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/aircraft")
def aircraft():
    return render_template("aircraft.html")


@app.route("/pricing")
def pricing():
    return render_template("pricing.html")


@app.route("/training")
def training():
    return render_template("training.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        location = request.form.get("location")
        interest = request.form.get("interest")
        timeline = request.form.get("timeline")
        model = request.form.get("model")
        aircraft_owner = request.form.get("aircraft_owner")
        message = request.form.get("message")

        email_message = EmailMessage()

        email_message["Subject"] = f"New CloudRider Lead — {name}"

        email_message["From"] = os.getenv("SMTP_USERNAME")

        email_message["To"] = os.getenv("INQUIRY_EMAIL")

        email_message.set_content(
            f"""
NEW CLOUDRIDER WEBSITE INQUIRY

Name:
{name}

Email:
{email}

Phone:
{phone}

Location:
{location}

Interest:
{interest}

Purchase Timeline:
{timeline}

Model:
{model}

Owned Aircraft Before:
{aircraft_owner}

Message:
{message}
"""
        )

        try:

            with smtplib.SMTP(
                os.getenv("SMTP_HOST"),
                int(os.getenv("SMTP_PORT", 587))
            ) as server:

                server.starttls()

                server.login(
                    os.getenv("SMTP_USERNAME"),
                    os.getenv("SMTP_PASSWORD")
                )

                server.send_message(email_message)

            flash(
                "Thanks! Your request has been sent. Someone from CloudRider Aviation will be in touch shortly.",
                "success"
            )

        except Exception as e:

            print("EMAIL ERROR:", e)

            flash(
                "We couldn't send your request right now. Please try again shortly.",
                "error"
            )

        return redirect(url_for("contact"))

    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)