import streamlit as st
import requests

def search_books(query, api_key=None):
    """Searches for books using the Google Books API.

    Args:
        query: The search query.
        api_key: The Google Books API key (optional).

    Returns:
        A dictionary containing the search results, or None if an error occurred.
    """
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {'q': query}

    if api_key:
        params['key'] = api_key
    else:
        st.error("API key is missing. Please add your Google Books API key to the secrets.")
        return None

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 403:
            st.error("HTTP 403 Forbidden: API key may be invalid or quota exceeded. Check your API key.")
        else:
            st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Request error occurred: {req_err}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
    return None

def main():
    st.title("Google Books Search App")
    st.write("Search for books by title using the Google Books API")

    # Input field for the book title
    query = st.text_input("Enter book title")

    # Retrieve API key securely from Streamlit secrets
    api_key = st.secrets.get("GOOGLE_BOOKS_API_KEY", None)

    if query:
        # Call the search_books function with the query and API key
        results = search_books(query, api_key)

        if results and 'items' in results:
            for item in results['items']:
                volume_info = item.get('volumeInfo', {})

                # Display book title or a default message
                st.write(f"### {volume_info.get('title', 'No Title Found')}")

                # Handle missing or multiple authors
                authors = ', '.join(volume_info.get('authors', ['Unknown Author']))
                st.write(f"**Author(s):** {authors}")

                # Display published date or a default message
                published_date = volume_info.get('publishedDate', 'N/A')
                st.write(f"**Published Date:** {published_date}")

                # Display book cover if available
                if 'imageLinks' in volume_info and 'thumbnail' in volume_info['imageLinks']:
                    st.image(volume_info['imageLinks']['thumbnail'], width=150)

                # Display book description or a default message
                description = volume_info.get('description', 'No description available.')
                st.write(f"**Description:** {description}")

                # Add a horizontal separator between books
                st.write("---")
        else:
            st.write("No books found. Please try another title.")

if __name__ == "__main__":
    main()
