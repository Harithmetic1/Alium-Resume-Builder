from app import create_app, db
from app import models

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': models.User,
        'Hobbies': models.Hobbies,
        'Skills': models.Skills,
        'Languages': models.Languages,
        'Education': models.Education,
        'Experience': models.Experience
    }


if __name__ == "__main__":
    app.run(debug=True)