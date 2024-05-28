from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

NOTES_FILE = 'notes.json'


def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r') as file:
            return json.load(file)
    return {}


def save_notes(notes):
    with open(NOTES_FILE, 'w') as file:
        json.dump(notes, file, indent=4)


@app.route('/')
def index():
    notes = load_notes()
    return render_template('index.html', notes=notes)


@app.route('/add', methods=['POST'])
def add_note():
    title = request.form['title']
    content = request.form['content']
    notes = load_notes()
    notes[title] = content
    save_notes(notes)
    return redirect(url_for('index'))


@app.route('/delete/<title>')
def delete_note(title):
    notes = load_notes()
    if title in notes:
        del notes[title]
        save_notes(notes)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)