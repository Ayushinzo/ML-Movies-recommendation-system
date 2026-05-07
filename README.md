# Movies Recommendation System

A small Flask-based chatbot project that uses OpenAI and various ML/NLP libraries to provide movie recommendations and basic chatbot functionality. It includes preprocessing, spell checking, recommendation logic, and a simple web UI.

**Key Features**
- **Chatbot:** Conversational interface (see `chatbot.py`).
- **Recommendations:** Movie recommendation engine using `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` (see `recommendation.py`).
- **Preprocessing & Spell Checking:** Helpers for text normalization and spelling (see `preprocessing.py`, `spell_checker.py`).
- **Simple Web UI:** Flask app entrypoint in `main.py` with templates in `templates/` and static assets in `static/`.

**Prerequisites**
- Python 3.8+
- A virtual environment is recommended

**Dependencies**
This project imports the following third-party Python modules across the codebase:

- **dotenv**: Environment variable management
- **openai**: OpenAI API client
- **flask**: Web framework
- **requests**: HTTP library
- **pandas**: Data manipulation
- **sklearn**: Scikit-learn for ML
- **nltk**: Natural Language Toolkit

You can install dependencies with:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
pip install -r requirements.txt
```

If `requirements.txt` is empty, install the modules directly:

```bash
pip install python-dotenv openai flask requests pandas scikit-learn nltk
```

**Environment Variables**
Create a `.env` file in the project root with at least:

```
OPENAI_API_KEY=your_openai_api_key
FLASK_ENV=development
```

**Running the App**
Start the Flask app (assuming the entrypoint is `main.py`):

```bash
python main.py
```

Or, if `main.py` uses `flask run`, use:

```bash
export FLASK_APP=main.py
flask run
```

**Project Structure**
- `main.py`: Application entrypoint and Flask server
- `chatbot.py`: Chatbot logic and OpenAI integration
- `recommendation.py`: Recommendation engine using TMDB datasets
- `preprocessing.py`: Text preprocessing utilities
- `spell_checker.py`: Spelling correction helpers
- `poster.py`: (likely) movie poster utilities or image handling
- `utility.py`: Misc helper functions
- `tmdb_5000_movies.csv`, `tmdb_5000_credits.csv`: Dataset files used by the recommender
- `templates/`: HTML templates (includes `index.html`)
- `static/`: Static assets (`script.js`, `style.css`)

**Notes & Next Steps**
- Populate `requirements.txt` with exact versions for reproducibility.
- If using `nltk`, ensure required corpora are downloaded (e.g., `punkt`, `wordnet`). Example:

```python
import nltk
nltk.download('punkt')
nltk.download('wordnet')
```

- If you want, I can generate a pinned `requirements.txt`, add example `.env`, or update `main.py` to provide clearer startup commands.

---

Created for the repository root. See the source files for implementation details.
